document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('csv-file');
    const fileInfo = document.getElementById('file-info');
    const filenameDisplay = document.getElementById('filename');
    const removeFileBtn = document.querySelector('.remove-file');
    const generateBtn = document.getElementById('generate-btn');
    const loadingIndicator = document.getElementById('loading-indicator');
    const uploadSection = document.getElementById('upload-section');
    const resultsContainer = document.getElementById('results-container');
    const resetBtn = document.getElementById('reset-btn');
    const scrollToUploadBtn = document.getElementById('scroll-to-upload');

    // --- FAQ Accordion ---
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');

            // Close all others
            faqItems.forEach(otherItem => {
                otherItem.classList.remove('active');
            });

            // Toggle current if it wasn't active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    let currentFile = null;

    // Scroll to upload section
    if (scrollToUploadBtn) {
        scrollToUploadBtn.addEventListener('click', () => {
            uploadSection.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Drag and Drop Events
    if (dropZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            dropZone.classList.add('dragover');
        }

        function unhighlight(e) {
            dropZone.classList.remove('dragover');
        }

        dropZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }

        // Click to upload
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', function () {
            handleFiles(this.files);
        });
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type === "text/csv" || file.name.endsWith('.csv')) {
                currentFile = file;
                updateUIWithFile(file);
            } else {
                alert("Please upload a valid CSV file.");
            }
        }
    }

    function updateUIWithFile(file) {
        filenameDisplay.textContent = file.name;
        dropZone.classList.add('hidden');
        fileInfo.classList.remove('hidden');
        generateBtn.disabled = false;
    }

    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', () => {
            currentFile = null;
            fileInput.value = '';
            dropZone.classList.remove('hidden');
            fileInfo.classList.add('hidden');
            generateBtn.disabled = true;
        });
    }

    // Generate Button Click
    if (generateBtn) {
        generateBtn.addEventListener('click', async () => {
            if (!currentFile) return;

            // Show loading
            generateBtn.classList.add('hidden');
            loadingIndicator.classList.remove('hidden');

            const formData = new FormData();
            formData.append('file', currentFile);

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.status === 'success') {
                    showResults(result);
                } else {
                    showErrorInUI(result.message);
                }

            } catch (error) {
                showErrorInUI("Network error: " + error.message);
            } finally {
                loadingIndicator.classList.add('hidden');
            }
        });
    }

    function showResults(data) {
        uploadSection.querySelector('.glass-card').classList.add('hidden');
        resultsContainer.classList.remove('hidden');

        document.getElementById('stat-total').textContent = data.total_rows || 0;
        document.getElementById('stat-processed').textContent = data.processed || 0;
        document.getElementById('stat-emails').textContent = data.email_sent || 0;

        // Render Generated Invoices
        const downloadList = document.getElementById('download-list');
        const downloadItems = document.getElementById('download-items');
        downloadItems.innerHTML = '';

        if (data.generated_invoices && data.generated_invoices.length > 0) {
            downloadList.classList.remove('hidden');
            data.generated_invoices.forEach(inv => {
                const li = document.createElement('li');

                const span = document.createElement('span');
                span.textContent = inv.client;

                const a = document.createElement('a');
                a.href = inv.url;
                a.className = 'download-link';
                a.target = '_blank';
                // Force download if possible, but for PDF viewed in browser is also fine.
                // a.download = ''; 
                a.innerHTML = '<i class="fas fa-file-pdf"></i> Download';

                li.appendChild(span);
                li.appendChild(a);
                downloadItems.appendChild(li);
            });
        } else {
            downloadList.classList.add('hidden');
        }

        const errorList = document.getElementById('error-list');
        const errorItems = document.getElementById('error-items');
        errorItems.innerHTML = '';

        if (data.errors && data.errors.length > 0) {
            errorList.classList.remove('hidden');
            data.errors.forEach(err => {
                const li = document.createElement('li');
                const rowInfo = err.row !== "N/A" ? `Row ${err.row}: ` : '';
                li.textContent = `${rowInfo}${err.errors.join(', ')}`;
                errorItems.appendChild(li);
            });
        } else {
            errorList.classList.add('hidden');
        }
    }

    function showErrorInUI(message) {
        alert("Error: " + message);
        generateBtn.classList.remove('hidden');
    }

    // Reset
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            currentFile = null;
            fileInput.value = '';
            dropZone.classList.remove('hidden');
            fileInfo.classList.add('hidden');
            generateBtn.disabled = true;
            generateBtn.classList.remove('hidden');

            uploadSection.querySelector('.glass-card').classList.remove('hidden');
            resultsContainer.classList.add('hidden');
            // Hide previous results
            document.getElementById('download-list').classList.add('hidden');
        });
    }

});

