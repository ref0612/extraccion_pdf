document.addEventListener('DOMContentLoaded', () => {
    const uploadForm     = document.getElementById('uploadForm');
    const uploadBtn      = document.getElementById('uploadBtn');
    const uploadSpinner  = document.getElementById('uploadSpinner');
    const startDateInput = document.getElementById('startDate');
    const endDateInput   = document.getElementById('endDate');
    let extractedTables  = [];

    // Inicializar rango Lunes–Domingo
    const today = new Date();
    const wd    = today.getDay();
    const offs  = (wd === 0 ? -6 : 1 - wd);
    const monday = new Date(today.setDate(today.getDate() + offs));
    const sunday = new Date(monday);
    sunday.setDate(monday.getDate() + 6);
    startDateInput.value = monday.toISOString().split('T')[0];
    endDateInput.value   = sunday.toISOString().split('T')[0];

    startDateInput.addEventListener('change', function() {
        try {
            // Get the raw input value (YYYY-MM-DD)
            const dateStr = this.value;
            
            // Parse the date manually to avoid timezone issues
            const [year, month, day] = dateStr.split('-').map(Number);
            
            // Create start date (month is 0-indexed in JavaScript Date)
            const startDate = new Date(year, month - 1, day);
            
            // Calculate end date (6 days after start date)
            const endDate = new Date(year, month - 1, day + 6);
            
            // Format date as YYYY-MM-DD
            const formatDate = (d) => {
                const y = d.getFullYear();
                const m = String(d.getMonth() + 1).padStart(2, '0');
                const day = String(d.getDate()).padStart(2, '0');
                return `${y}-${m}-${day}`;
            };
            
            // Set the end date input value
            endDateInput.value = formatDate(endDate);
            
            // Debug output
            console.log('Start date:', formatDate(startDate), 
                       '(Day of week:', ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'][startDate.getDay()] + ')');
            console.log('End date:  ', formatDate(endDate), 
                       '(Day of week:', ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'][endDate.getDay()] + ')');
            
        } catch (error) {
            console.error('Error calculating date range:', error);
        }
    });

    uploadForm.addEventListener('submit', async e => {
        e.preventDefault();
        const formData = new FormData(uploadForm);
        formData.append('start_date', startDateInput.value);
        formData.append('end_date',   endDateInput.value);

        uploadBtn.disabled = true;
        uploadSpinner.classList.remove('d-none');
        clearResults();

        try {
            const res = await fetch('/upload', { method: 'POST', body: formData });
            const json = await res.json();

            if (res.ok && json.success) {
                extractedTables = json.tables;
                displayResults(json.metadata, json.tables);
                showAlert('PDF procesado correctamente', 'success');
            } else {
                showAlert(json.error || json.warning, 'danger');
            }
        } catch (err) {
            showAlert('Error de conexión: ' + err.message, 'danger');
        } finally {
            uploadBtn.disabled = false;
            uploadSpinner.classList.add('d-none');
        }
    });

    function displayResults(meta, tables) {
        document.getElementById('totalPages').textContent      = meta.total_pages;
        document.getElementById('tablesExtracted').textContent = meta.extracted_tables;
        document.getElementById('extractionDate').textContent  = meta.extraction_date;
        document.getElementById('periodDates').textContent     =
            `${startDateInput.value} – ${endDateInput.value}`;

        document.getElementById('resultsSection').classList.remove('d-none');
        document.getElementById('documentInfo').classList.remove('d-none');
        document.getElementById('exportButtons').classList.toggle('d-none', tables.length === 0);

        const container = document.getElementById('tablesContainer');
        container.innerHTML = '';
        tables.forEach((t, i) => container.appendChild(createTableCard(t, i)));
    }

    function clearResults() {
        document.getElementById('resultsSection').classList.add('d-none');
        document.getElementById('exportButtons').classList.add('d-none');
        document.getElementById('alertContainer').innerHTML = '';
        document.getElementById('tablesContainer').innerHTML = '';
    }

    function createTableCard(table, idx) {
        const card = document.createElement('div');
        card.className = 'card mb-4';
        const tblId = `table-${idx}`;
        card.innerHTML = `
          <div class="card-body">
            <h5 class="card-title">Tabla ${idx+1} – Página ${table.page}</h5>
            <p>${table.rows} filas × ${table.columns} columnas</p>
            <div class="table-responsive">
              <table id="${tblId}" class="table table-striped table-bordered" style="width:100%">
                <thead><tr>${table.headers.map(h => `<th>${h}</th>`).join('')}</tr></thead>
              </table>
            </div>
          </div>`;
        setTimeout(() => {
            $(`#${tblId}`).DataTable({
                data: table.data,
                columns: table.headers.map(title => ({ title })),
                pageLength: 10,
                lengthMenu: [[10,25,50,-1],[10,25,50,"Todos"]],
                language: { url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json' },
                responsive: true,
                destroy: true
            });
        }, 50);
        return card;
    }

    document.getElementById('exportExcel').addEventListener('click', () => exportData('excel'));
    document.getElementById('exportCSV').addEventListener('click', () => exportData('csv'));

    async function exportData(fmt) {
        if (!extractedTables.length) {
            showAlert('No hay datos para exportar', 'warning');
            return;
        }
        try {
            const resp = await fetch(`/export/${fmt}`, {
                method: 'POST',
                headers: { 'Content-Type':'application/json' },
                body: JSON.stringify({ tables: extractedTables })
            });
            const j = await resp.json();
            if (j.success) {
                window.location = `/download/${j.filename}`;
            } else {
                showAlert(j.error, 'danger');
            }
        } catch (e) {
            showAlert('Error al exportar: ' + e.message, 'danger');
        }
    }

    function showAlert(msg, type='info') {
        const c = document.getElementById('alertContainer');
        const div = document.createElement('div');
        div.className = `alert alert-${type} alert-dismissible fade show`;
        div.innerHTML = msg + `<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
        c.appendChild(div);
        setTimeout(()=> $(div).alert('close'), 5000);
    }
});
