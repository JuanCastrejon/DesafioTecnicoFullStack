<?php
$apiBaseUrl = getenv('API_BASE_URL');
$host = $_SERVER['HTTP_HOST'] ?? '';
$isVercelPreviewPhpClient = str_starts_with($host, 'php-client-git-') && str_ends_with($host, '.vercel.app');

if ($apiBaseUrl === false || $apiBaseUrl === '' || $apiBaseUrl === null) {
  $apiBaseUrl = $isVercelPreviewPhpClient
    ? 'https://desafio-tecnico-full-stack.vercel.app'
    : 'http://127.0.0.1:8010';
}

$apiBaseUrl = rtrim($apiBaseUrl, '/');
?>
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Demo Eventos - Prueba Tecnica</title>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
    crossorigin="anonymous"
  />
  <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <link rel="stylesheet" href="assets/styles/demo.css" />
</head>
<body>
  <main class="app-shell">
    <section class="hero-panel">
      <span class="hero-kicker">Demostracion funcional</span>
      <h1 class="hero-title">Consulta de Eventos</h1>
      <p class="hero-subtitle">Listado paginado con filtros por fecha y visualizacion de detalle en tiempo real.</p>
      <div class="hero-metrics">
        <div class="metric-item">
          <div class="metric-label">Stack</div>
          <div class="metric-value">PHP + jQuery</div>
        </div>
        <div class="metric-item">
          <div class="metric-label">Consumo</div>
          <div class="metric-value">API REST en vivo</div>
        </div>
      </div>
    </section>

    <section class="card surface-card filters-card mb-4">
      <div class="card-body">
        <form id="filtersForm" class="filters-form">
          <div class="filter-group">
            <label class="form-label" for="fromDateDisplay">Desde</label>
            <div class="datepicker-wrapper" data-datepicker="from">
              <input type="hidden" id="fromDate" name="fromDate" />
              <button type="button" class="datepicker-trigger" id="fromDateDisplay">
                <svg class="datepicker-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                <span class="datepicker-text">Seleccionar fecha</span>
              </button>
              <div class="datepicker-dropdown">
                <div class="datepicker-header">
                  <button type="button" class="datepicker-nav datepicker-prev" aria-label="Mes anterior">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <polyline points="15 18 9 12 15 6"></polyline>
                    </svg>
                  </button>
                  <span class="datepicker-month-year"></span>
                  <button type="button" class="datepicker-nav datepicker-next" aria-label="Mes siguiente">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                  </button>
                </div>
                <div class="datepicker-weekdays">
                  <span>Do</span><span>Lu</span><span>Ma</span><span>Mi</span><span>Ju</span><span>Vi</span><span>Sa</span>
                </div>
                <div class="datepicker-days"></div>
                <div class="datepicker-footer">
                  <button type="button" class="datepicker-clear">Limpiar</button>
                  <button type="button" class="datepicker-today">Hoy</button>
                </div>
              </div>
            </div>
          </div>

          <div class="filter-group">
            <label class="form-label" for="toDateDisplay">Hasta</label>
            <div class="datepicker-wrapper" data-datepicker="to">
              <input type="hidden" id="toDate" name="toDate" />
              <button type="button" class="datepicker-trigger" id="toDateDisplay">
                <svg class="datepicker-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                <span class="datepicker-text">Seleccionar fecha</span>
              </button>
              <div class="datepicker-dropdown">
                <div class="datepicker-header">
                  <button type="button" class="datepicker-nav datepicker-prev" aria-label="Mes anterior">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <polyline points="15 18 9 12 15 6"></polyline>
                    </svg>
                  </button>
                  <span class="datepicker-month-year"></span>
                  <button type="button" class="datepicker-nav datepicker-next" aria-label="Mes siguiente">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                  </button>
                </div>
                <div class="datepicker-weekdays">
                  <span>Do</span><span>Lu</span><span>Ma</span><span>Mi</span><span>Ju</span><span>Vi</span><span>Sa</span>
                </div>
                <div class="datepicker-days"></div>
                <div class="datepicker-footer">
                  <button type="button" class="datepicker-clear">Limpiar</button>
                  <button type="button" class="datepicker-today">Hoy</button>
                </div>
              </div>
            </div>
          </div>

          <div class="filter-group filter-group-size">
            <label class="form-label" for="pageSize">Tamaño</label>
            <select id="pageSize" class="form-select">
              <option value="10" selected>10</option>
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>

          <div class="filter-group filter-group-actions">
            <button type="submit" class="btn btn-cta">
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              Filtrar
            </button>
            <button type="button" id="resetFilters" class="btn btn-ghost">
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
              </svg>
              Limpiar
            </button>
          </div>
        </form>
      </div>
    </section>

    <section class="card surface-card">
      <div class="card-body">
        <div class="results-header d-flex justify-content-between align-items-center">
          <span id="statusPill" class="status-pill status-idle">Listo</span>
          <strong id="resultMeta">Total: 0</strong>
        </div>

        <div id="alertBox" class="alert alert-danger d-none" role="alert"></div>

        <div class="table-wrap">
          <table class="table table-hover mb-0 align-middle">
            <thead class="sticky-top">
              <tr>
                <th style="width: 90px;">ID</th>
                <th>Titulo</th>
                <th style="width: 220px;">Fecha</th>
                <th style="width: 120px;">Accion</th>
              </tr>
            </thead>
            <tbody id="eventsBody">
              <tr>
                <td colspan="4" class="text-center py-4 text-muted">Sin datos por ahora.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pager-wrap d-flex justify-content-between align-items-center mt-3">
          <button id="prevPage" class="btn btn-page" type="button">Anterior</button>
          <span id="pageInfo">Pagina 1</span>
          <button id="nextPage" class="btn btn-page" type="button">Siguiente</button>
        </div>
      </div>
    </section>
  </main>

  <div class="modal fade" id="eventDetailModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title fs-5" id="eventModalTitle">Detalle del evento</h2>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <dl class="row mb-0">
            <dt class="col-sm-3">ID</dt>
            <dd class="col-sm-9" id="detailId">-</dd>

            <dt class="col-sm-3">Titulo</dt>
            <dd class="col-sm-9" id="detailTitle">-</dd>

            <dt class="col-sm-3">Descripcion</dt>
            <dd class="col-sm-9" id="detailDescription">-</dd>

            <dt class="col-sm-3">Fecha</dt>
            <dd class="col-sm-9" id="detailDate">-</dd>

            <dt class="col-sm-3">Direccion</dt>
            <dd class="col-sm-9" id="detailAddress">-</dd>

            <dt class="col-sm-3">Latitud</dt>
            <dd class="col-sm-9" id="detailLat">-</dd>

            <dt class="col-sm-3">Longitud</dt>
            <dd class="col-sm-9" id="detailLng">-</dd>
          </dl>
        </div>
      </div>
    </div>
  </div>

  <script
    src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
    crossorigin="anonymous"
  ></script>
  <script>
    const API_BASE_URL = <?php echo json_encode($apiBaseUrl, JSON_UNESCAPED_SLASHES); ?>;

    const state = {
      page: 1,
      size: 10,
      total: 0,
      from: '',
      to: ''
    };

    // ========== Modern Datepicker ==========
    const MONTHS_ES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                       'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];

    class DatePicker {
      constructor(wrapper) {
        this.wrapper = wrapper;
        this.type = wrapper.dataset.datepicker;
        this.hiddenInput = wrapper.querySelector('input[type="hidden"]');
        this.trigger = wrapper.querySelector('.datepicker-trigger');
        this.dropdown = wrapper.querySelector('.datepicker-dropdown');
        this.monthYearLabel = wrapper.querySelector('.datepicker-month-year');
        this.daysContainer = wrapper.querySelector('.datepicker-days');
        this.prevBtn = wrapper.querySelector('.datepicker-prev');
        this.nextBtn = wrapper.querySelector('.datepicker-next');
        this.clearBtn = wrapper.querySelector('.datepicker-clear');
        this.todayBtn = wrapper.querySelector('.datepicker-today');
        this.textSpan = wrapper.querySelector('.datepicker-text');

        this.currentDate = new Date();
        this.selectedDate = null;
        this.viewYear = this.currentDate.getFullYear();
        this.viewMonth = this.currentDate.getMonth();

        this.init();
      }

      init() {
        this.trigger.addEventListener('click', (e) => {
          e.preventDefault();
          this.toggle();
        });

        this.prevBtn.addEventListener('click', (e) => {
          e.preventDefault();
          this.prevMonth();
        });

        this.nextBtn.addEventListener('click', (e) => {
          e.preventDefault();
          this.nextMonth();
        });

        this.clearBtn.addEventListener('click', (e) => {
          e.preventDefault();
          this.clear();
        });

        this.todayBtn.addEventListener('click', (e) => {
          e.preventDefault();
          this.selectToday();
        });

        document.addEventListener('click', (e) => {
          if (!this.wrapper.contains(e.target)) {
            this.close();
          }
        });

        this.render();
      }

      toggle() {
        if (this.wrapper.classList.contains('open')) {
          this.close();
        } else {
          this.open();
        }
      }

      open() {
        document.querySelectorAll('.datepicker-wrapper.open').forEach(w => {
          if (w !== this.wrapper) w.classList.remove('open');
        });
        this.wrapper.classList.add('open');
        if (this.selectedDate) {
          this.viewYear = this.selectedDate.getFullYear();
          this.viewMonth = this.selectedDate.getMonth();
        }
        this.render();
      }

      close() {
        this.wrapper.classList.remove('open');
      }

      prevMonth() {
        this.viewMonth--;
        if (this.viewMonth < 0) {
          this.viewMonth = 11;
          this.viewYear--;
        }
        this.render();
      }

      nextMonth() {
        this.viewMonth++;
        if (this.viewMonth > 11) {
          this.viewMonth = 0;
          this.viewYear++;
        }
        this.render();
      }

      selectDate(year, month, day) {
        this.selectedDate = new Date(year, month, day);
        const iso = this.formatISO(this.selectedDate);
        this.hiddenInput.value = iso;
        this.textSpan.textContent = this.formatDisplay(this.selectedDate);
        this.trigger.classList.add('has-value');
        this.close();
        this.render();
      }

      clear() {
        this.selectedDate = null;
        this.hiddenInput.value = '';
        this.textSpan.textContent = 'Seleccionar fecha';
        this.trigger.classList.remove('has-value');
        this.viewYear = this.currentDate.getFullYear();
        this.viewMonth = this.currentDate.getMonth();
        this.render();
      }

      selectToday() {
        const today = new Date();
        this.selectDate(today.getFullYear(), today.getMonth(), today.getDate());
      }

      formatISO(date) {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
      }

      formatDisplay(date) {
        const d = date.getDate();
        const m = MONTHS_ES[date.getMonth()].substring(0, 3);
        const y = date.getFullYear();
        return `${d} ${m} ${y}`;
      }

      render() {
        this.monthYearLabel.textContent = `${MONTHS_ES[this.viewMonth]} ${this.viewYear}`;
        
        const firstDay = new Date(this.viewYear, this.viewMonth, 1);
        const lastDay = new Date(this.viewYear, this.viewMonth + 1, 0);
        const startDayOfWeek = firstDay.getDay();
        const daysInMonth = lastDay.getDate();

        const prevMonthLastDay = new Date(this.viewYear, this.viewMonth, 0).getDate();

        let html = '';

        for (let i = startDayOfWeek - 1; i >= 0; i--) {
          const day = prevMonthLastDay - i;
          const prevMonth = this.viewMonth === 0 ? 11 : this.viewMonth - 1;
          const prevYear = this.viewMonth === 0 ? this.viewYear - 1 : this.viewYear;
          html += `<button type="button" class="datepicker-day other-month" data-year="${prevYear}" data-month="${prevMonth}" data-day="${day}">${day}</button>`;
        }

        const today = new Date();
        for (let day = 1; day <= daysInMonth; day++) {
          let classes = 'datepicker-day';
          
          if (today.getFullYear() === this.viewYear && 
              today.getMonth() === this.viewMonth && 
              today.getDate() === day) {
            classes += ' today';
          }

          if (this.selectedDate &&
              this.selectedDate.getFullYear() === this.viewYear &&
              this.selectedDate.getMonth() === this.viewMonth &&
              this.selectedDate.getDate() === day) {
            classes += ' selected';
          }

          html += `<button type="button" class="${classes}" data-year="${this.viewYear}" data-month="${this.viewMonth}" data-day="${day}">${day}</button>`;
        }

        const totalCells = startDayOfWeek + daysInMonth;
        const remaining = totalCells % 7 === 0 ? 0 : 7 - (totalCells % 7);
        const nextMonth = this.viewMonth === 11 ? 0 : this.viewMonth + 1;
        const nextYear = this.viewMonth === 11 ? this.viewYear + 1 : this.viewYear;
        
        for (let day = 1; day <= remaining; day++) {
          html += `<button type="button" class="datepicker-day other-month" data-year="${nextYear}" data-month="${nextMonth}" data-day="${day}">${day}</button>`;
        }

        this.daysContainer.innerHTML = html;

        this.daysContainer.querySelectorAll('.datepicker-day').forEach(btn => {
          btn.addEventListener('click', (e) => {
            e.preventDefault();
            const year = parseInt(btn.dataset.year);
            const month = parseInt(btn.dataset.month);
            const day = parseInt(btn.dataset.day);
            this.selectDate(year, month, day);
          });
        });
      }
    }

    const datepickers = {};

    const detailModal = new bootstrap.Modal(document.getElementById('eventDetailModal'));

    function formatDate(value) {
      if (!value) return '-';
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return value;
      return date.toLocaleString('es-CO', { hour12: false });
    }

    function setStatus(text, tone) {
      const statusPill = $('#statusPill');
      statusPill.text(text);
      statusPill.removeClass('status-idle status-loading status-error status-success');

      if (tone === 'error') {
        statusPill.addClass('status-error');
      } else if (tone === 'success') {
        statusPill.addClass('status-success');
      } else if (String(text).toLowerCase().includes('cargando') || String(text).toLowerCase().includes('consultando')) {
        statusPill.addClass('status-loading');
      } else {
        statusPill.addClass('status-idle');
      }
    }

    function setAlert(message) {
      const alertBox = $('#alertBox');
      if (!message) {
        alertBox.addClass('d-none').text('');
        return;
      }

      alertBox.removeClass('d-none').text(message);
    }

    function renderRows(events) {
      const body = $('#eventsBody');
      body.empty();

      if (!events.length) {
        body.append('<tr><td colspan="4" class="text-center py-4 text-muted">No hay eventos para los filtros seleccionados.</td></tr>');
        return;
      }

      events.forEach((eventItem) => {
        const tr = $('<tr class="clickable-row"></tr>');
        tr.append($('<td></td>').text(eventItem.id));
        tr.append($('<td></td>').text(eventItem.title));
        tr.append($('<td></td>').text(formatDate(eventItem.date)));

        const actionTd = $('<td></td>');
        const detailBtn = $('<button type="button" class="btn btn-sm btn-row-action">Ver detalle</button>');
        detailBtn.on('click', function (ev) {
          ev.stopPropagation();
          loadEventDetail(eventItem.id);
        });
        actionTd.append(detailBtn);
        tr.append(actionTd);

        tr.on('click', function () {
          loadEventDetail(eventItem.id);
        });

        body.append(tr);
      });
    }

    function updatePaginationMeta() {
      const lastPage = Math.max(1, Math.ceil(state.total / state.size));
      $('#pageInfo').text(`Pagina ${state.page} de ${lastPage}`);
      $('#resultMeta').text(`Total: ${state.total}`);
      $('#prevPage').prop('disabled', state.page <= 1);
      $('#nextPage').prop('disabled', state.page >= lastPage);
    }

    function buildQueryParams() {
      const params = new URLSearchParams();
      params.set('page', String(state.page));
      params.set('size', String(state.size));

      if (state.from) {
        params.set('from', state.from);
      }

      if (state.to) {
        params.set('to', state.to);
      }

      return params.toString();
    }

    function loadEvents() {
      setStatus('Cargando...', '');
      setAlert('');

      $.ajax({
        url: `${API_BASE_URL}/events?${buildQueryParams()}`,
        method: 'GET',
        dataType: 'json'
      })
        .done(function (response) {
          const events = response.data || [];
          state.total = (response.meta && response.meta.total) || 0;

          renderRows(events);
          updatePaginationMeta();
          setStatus('Datos cargados', 'success');
        })
        .fail(function (xhr) {
          const detail = xhr.responseJSON && xhr.responseJSON.detail ? String(xhr.responseJSON.detail) : 'No fue posible cargar eventos.';
          setStatus('Error al cargar', 'error');
          setAlert(detail);
          renderRows([]);
          state.total = 0;
          updatePaginationMeta();
        });
    }

    function loadEventDetail(eventId) {
      setAlert('');
      setStatus(`Consultando detalle #${eventId}...`, '');

      $.ajax({
        url: `${API_BASE_URL}/events/${eventId}`,
        method: 'GET',
        dataType: 'json'
      })
        .done(function (eventItem) {
          $('#eventModalTitle').text(`Detalle evento #${eventItem.id}`);
          $('#detailId').text(eventItem.id);
          $('#detailTitle').text(eventItem.title || '-');
          $('#detailDescription').text(eventItem.description || '-');
          $('#detailDate').text(formatDate(eventItem.date));
          $('#detailAddress').text(eventItem.location && eventItem.location.address ? eventItem.location.address : '-');
          $('#detailLat').text(eventItem.location && eventItem.location.lat ? eventItem.location.lat : '-');
          $('#detailLng').text(eventItem.location && eventItem.location.lng ? eventItem.location.lng : '-');
          setStatus('Detalle cargado', 'success');
          detailModal.show();
        })
        .fail(function (xhr) {
          const detail = xhr.responseJSON && xhr.responseJSON.detail ? String(xhr.responseJSON.detail) : `No fue posible cargar el evento ${eventId}.`;
          setStatus('Error en detalle', 'error');
          setAlert(detail);
        });
    }

    $(function () {
      // Initialize datepickers
      document.querySelectorAll('.datepicker-wrapper').forEach(wrapper => {
        const type = wrapper.dataset.datepicker;
        datepickers[type] = new DatePicker(wrapper);
      });

      $('#filtersForm').on('submit', function (event) {
        event.preventDefault();
        state.from = String($('#fromDate').val() || '');
        state.to = String($('#toDate').val() || '');
        state.size = Number($('#pageSize').val() || 10);
        state.page = 1;
        loadEvents();
      });

      $('#resetFilters').on('click', function () {
        // Clear datepickers
        Object.values(datepickers).forEach(dp => dp.clear());
        $('#pageSize').val('10');
        state.from = '';
        state.to = '';
        state.size = 10;
        state.page = 1;
        loadEvents();
      });

      $('#prevPage').on('click', function () {
        if (state.page > 1) {
          state.page -= 1;
          loadEvents();
        }
      });

      $('#nextPage').on('click', function () {
        const lastPage = Math.max(1, Math.ceil(state.total / state.size));
        if (state.page < lastPage) {
          state.page += 1;
          loadEvents();
        }
      });

      loadEvents();
    });
  </script>
</body>
</html>

