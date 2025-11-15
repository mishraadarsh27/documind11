// DocuMind Web Application - Frontend JavaScript

let currentDocumentId = null;
let currentSummaries = {};

// Tab switching
function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    if (tab === 'file') {
        document.querySelector('.tab-btn:first-child').classList.add('active');
        document.getElementById('fileTab').classList.add('active');
    } else {
        document.querySelector('.tab-btn:last-child').classList.add('active');
        document.getElementById('urlTab').classList.add('active');
    }
}

// File upload form
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    const checkboxes = document.querySelectorAll('#fileTab input[name="tasks"]:checked');
    const tasks = Array.from(checkboxes).map(cb => cb.value);
    formData.append('tasks', tasks.join(','));
    
    await processDocument(formData, 'file');
});

// URL form
document.getElementById('urlForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert('Please enter a URL');
        return;
    }
    
    const checkboxes = document.querySelectorAll('#urlTab input[name="tasks"]:checked');
    const tasks = Array.from(checkboxes).map(cb => cb.value);
    
    const data = {
        url: url,
        tasks: tasks
    };
    
    await processDocument(data, 'url');
});

// Process document
async function processDocument(data, type) {
    showLoading();
    
    try {
        const url = type === 'file' ? '/api/process' : '/api/process-url';
        const options = type === 'file' 
            ? { method: 'POST', body: data }
            : {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            };
        
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Processing failed');
        }
        
        currentDocumentId = result.document_id;
        currentSummaries = result.summaries || {};
        
        displayResults(result);
        hideLoading();
        
    } catch (error) {
        hideLoading();
        alert('Error: ' + error.message);
        console.error(error);
    }
}

// Display results
function displayResults(result) {
    // Hide upload section, show results
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
    
    // Display metadata
    displayMetadata(result.metadata);
    
    // Display extractions
    displayExtractions(result.extractions);
    
    // Display summaries
    if (result.summaries) {
        displaySummaries(result.summaries);
    }
    
    // Show Q&A if enabled
    if (result.has_qa) {
        document.getElementById('qaCard').style.display = 'block';
        setupQA();
    }
}

// Display metadata
function displayMetadata(metadata) {
    const container = document.getElementById('metadataContent');
    container.innerHTML = '';
    
    const items = [
        { label: 'Source', value: metadata.source || 'N/A' },
        { label: 'Type', value: metadata.source_type || 'N/A' },
        { label: 'Pages', value: metadata.total_pages || 'N/A' },
        { label: 'Words', value: metadata.total_words?.toLocaleString() || 'N/A' },
        { label: 'Characters', value: metadata.total_chars?.toLocaleString() || 'N/A' }
    ];
    
    items.forEach(item => {
        const div = document.createElement('div');
        div.className = 'metadata-item';
        div.innerHTML = `
            <div class="metadata-label">${item.label}</div>
            <div class="metadata-value">${item.value}</div>
        `;
        container.appendChild(div);
    });
}

// Display extractions
function displayExtractions(extractions) {
    const container = document.getElementById('extractionsContent');
    container.innerHTML = '';
    
    const items = [
        { label: 'Tables', count: extractions.tables_count || 0 },
        { label: 'Metrics', count: extractions.metrics_count || 0 },
        { label: 'Dates', count: extractions.dates_count || 0 },
        { label: 'Tasks', count: extractions.tasks_count || 0 },
        { label: 'Entities', count: extractions.entities_count || 0 }
    ];
    
    items.forEach(item => {
        const div = document.createElement('div');
        div.className = 'extraction-item';
        div.innerHTML = `
            <div class="extraction-count">${item.count}</div>
            <div class="extraction-label">${item.label}</div>
        `;
        container.appendChild(div);
    });
}

// Display summaries
function displaySummaries(summaries) {
    currentSummaries = summaries;
    showSummary('executive');
}

// Show specific summary
function showSummary(type) {
    // Update tabs
    document.querySelectorAll('.summary-tab').forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    // Show content
    const container = document.getElementById('summaryContent');
    const summary = currentSummaries[type] || 'Summary not available';
    container.textContent = summary;
}

// Setup Q&A
function setupQA() {
    document.getElementById('qaForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const question = document.getElementById('questionInput').value;
        if (!question) return;
        
        try {
            const response = await fetch('/api/qa', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    document_id: currentDocumentId,
                    question: question
                })
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Failed to get answer');
            }
            
            displayQA(question, result);
            document.getElementById('questionInput').value = '';
            
        } catch (error) {
            alert('Error: ' + error.message);
            console.error(error);
        }
    });
}

// Display Q&A result
function displayQA(question, answer) {
    const container = document.getElementById('qaResults');
    
    const div = document.createElement('div');
    div.className = 'qa-item';
    
    let citationsHtml = '';
    if (answer.citations && answer.citations.length > 0) {
        citationsHtml = '<div class="qa-citations"><strong>Citations:</strong>';
        answer.citations.forEach(cit => {
            citationsHtml += `<div class="citation-item">Page ${cit.page}: ${cit.text.substring(0, 100)}...</div>`;
        });
        citationsHtml += '</div>';
    }
    
    div.innerHTML = `
        <div class="qa-question">Q: ${question}</div>
        <div class="qa-answer">${answer.answer}</div>
        <div class="qa-confidence">Confidence: ${(answer.confidence * 100).toFixed(1)}%</div>
        ${citationsHtml}
    `;
    
    container.insertBefore(div, container.firstChild);
}

// Reset view
function resetView() {
    document.getElementById('uploadSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('fileInput').value = '';
    document.getElementById('urlInput').value = '';
    document.getElementById('qaResults').innerHTML = '';
    currentDocumentId = null;
    currentSummaries = {};
}

// Loading functions
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// Health check on load
fetch('/api/health')
    .then(res => res.json())
    .then(data => {
        if (!data.api_key_set) {
            console.warn('OpenAI API key not set. Some features may not work.');
        }
    })
    .catch(err => console.error('Health check failed:', err));

