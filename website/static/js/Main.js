document.getElementById('cloned-voice').addEventListener('change', async function() {
    const voiceId = this.value;
    const projectId = this.dataset.projectId;
    const statusElement = document.getElementById('voice-status');
    
    statusElement.textContent = "Saving...";
    statusElement.className = "status-message saving";
    
    try {
        const response = await fetch(`/assign_voice/${projectId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ voice_id: voiceId })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to save voice');
        }
        
        statusElement.textContent = data.voice_name ? `✓ ${data.voice_name}` : "✓ Voice removed";
        statusElement.className = "status-message success";
        
        setTimeout(() => {
            statusElement.textContent = "";
            statusElement.className = "status-message";
        }, 3000);
        
    } catch (error) {
        console.error('Error:', error);
        statusElement.textContent = `✗ ${error.message}`;
        statusElement.className = "status-message error";
        this.value = this.dataset.previousValue || '';
    }
    
    this.dataset.previousValue = this.value;
});

// Load surahs when page loads
document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Load surahs into dropdown
        const surahResponse = await fetch('/get_surahs');
        const surahs = await surahResponse.json();
        
        const surahSelect = document.getElementById('sura-select');
        surahSelect.innerHTML = '<option disabled selected>Select Sura</option>';
        
        surahs.forEach(surah => {
            const option = document.createElement('option');
            option.value = surah.id;
            option.textContent = `${surah.number}. ${surah.name} (${surah.arabic_name}) - ${surah.ayah_count} ayahs`;
            surahSelect.appendChild(option);
        });
        
        // Handle surah selection
        surahSelect.addEventListener('change', async function() {
            const surahId = this.value;
            if (!surahId) return;
            
            try {
                const verseResponse = await fetch(`/get_verses/${surahId}`);
                const verses = await verseResponse.json();
                
                const ayahContainer = document.getElementById('ayah-container');
                ayahContainer.style.display = 'block';
                ayahContainer.innerHTML = '';
                
                // Display each verse
                verses.forEach(verse => {
                    const verseDiv = document.createElement('div');
                    verseDiv.className = 'verse';
                    verseDiv.innerHTML = `
                        <p class="verse-number">${verse.number}</p>
                        <p class="verse-text">${verse.text}</p>
                    `;
                    ayahContainer.appendChild(verseDiv);
                });
                
            } catch (error) {
                console.error('Error loading verses:', error);
            }
        });
        
    } catch (error) {
        console.error('Error loading surahs:', error);
    }
});

