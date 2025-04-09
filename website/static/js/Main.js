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
