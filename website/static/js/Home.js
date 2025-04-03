document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const addProjectBtn = document.getElementById('addProjectBtn');
    const projectModal = document.getElementById('projectModal');
    const closeModal = document.getElementById('closeModal');
    const projectForm = document.getElementById('projectForm');
    const projectsGrid = document.getElementById('projectsGrid');
    const deleteModal = document.getElementById('deleteModal');
    const closeDeleteModal = document.getElementById('closeDeleteModal');
    const confirmDeleteBtn = document.getElementById('confirmDelete');
    const cancelDeleteBtn = document.getElementById('cancelDelete');

    // State variables
    let projectToDelete = null;

    // Event Listeners
    addProjectBtn.addEventListener('click', openModal);
    closeModal.addEventListener('click', closeModalHandler);
    closeDeleteModal.addEventListener('click', closeDeleteModalHandler);
    projectForm.addEventListener('submit', handleProjectSubmit);
    confirmDeleteBtn.addEventListener('click', confirmDelete);
    cancelDeleteBtn.addEventListener('click', closeDeleteModalHandler);

    // Handle delete button clicks (delegated event)
    projectsGrid.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-btn')) {
            e.stopPropagation(); // Prevent card click from triggering
            projectToDelete = e.target.getAttribute('data-id');
            deleteModal.style.display = 'block';
        }
        
        // Handle project card click (navigation)
        if (e.target.closest('.project-card') && !e.target.classList.contains('delete-btn')) {
            const projectId = e.target.closest('.project-card').getAttribute('data-id');
            // Navigate to project details page
            window.location.href = `/project/${projectId}`;
        }
    });

    // Modal Functions
    function openModal() {
        projectModal.style.display = 'block';
    }

    function closeModalHandler() {
        projectModal.style.display = 'none';
        projectForm.reset();
    }

    function closeDeleteModalHandler() {
        deleteModal.style.display = 'none';
        projectToDelete = null;
    }

    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === projectModal) {
            closeModalHandler();
        }
        if (e.target === deleteModal) {
            closeDeleteModalHandler();
        }
    });

    // Form Submission
    async function handleProjectSubmit(e) {
        e.preventDefault();
        
        const projectName = document.getElementById('projectName').value;
        const translatedVersion = document.getElementById('translatedVersion').value;
        const language = document.getElementById('language').value;

        try {
            const response = await fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: projectName,
                    translated_version: translatedVersion,
                    language: language
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Reload the page to show the new project
                window.location.reload();
            } else {
                alert(data.error || 'Failed to create project');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while creating the project');
        }
    }

    // Delete Project
    async function confirmDelete() {
        if (!projectToDelete) return;

        try {
            const response = await fetch(`/delete_project/${projectToDelete}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.ok) {
                // Remove the project card from the DOM
                const projectCard = document.querySelector(`.project-card[data-id="${projectToDelete}"]`);
                if (projectCard) {
                    projectCard.remove();
                }
            } else {
                alert(data.error || 'Failed to delete project');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while deleting the project');
        } finally {
            closeDeleteModalHandler();
        }
    }
});
// Store versions data globally
let quranVersionsData = [];

async function loadQuranVersions() {
    try {
        const response = await fetch('/get_quran_versions');
        quranVersionsData = await response.json();
        
        const versionSelect = document.getElementById('translatedVersion');
        versionSelect.innerHTML = '<option value="" disabled selected>Select Translated Version</option>';
        
        quranVersionsData.forEach(version => {
            const option = document.createElement('option');
            option.value = version.name;
            option.textContent = version.name;
            versionSelect.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error loading Quran versions:', error);
        document.getElementById('translatedVersion').innerHTML = 
            '<option value="" disabled selected>Error loading versions</option>';
    }
}

document.getElementById('translatedVersion').addEventListener('change', function() {
    const selectedVersion = quranVersionsData.find(v => v.name === this.value);
    const languageSelect = document.getElementById('language');
    
    if (selectedVersion) {
        languageSelect.innerHTML = `
            <option value="${selectedVersion.language}" selected>
                ${selectedVersion.language}
            </option>
        `;
        languageSelect.disabled = true;
    } else {
        languageSelect.innerHTML = `
            <option value="" disabled selected>Select Language</option>
            <option value="English">English</option>
            <option value="Arabic">Arabic</option>
        `;
        languageSelect.disabled = false;
    }
});

// Initialize when modal opens
document.getElementById('addProjectBtn').addEventListener('click', loadQuranVersions);