<?php
$apiBaseUrl = getenv('API_BASE_URL') ?: 'http://localhost:8000';
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
  <style>
    body {
      background: linear-gradient(180deg, #f5f7fb 0%, #eef2f8 100%);
      min-height: 100vh;
    }

    .app-shell {
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px 16px 48px;
    }

    .card-soft {
      border: 0;
      border-radius: 14px;
      box-shadow: 0 10px 30px rgba(20, 32, 62, 0.08);
    }

    .table-wrap {
      max-height: 560px;
      overflow: auto;
    }

    .clickable-row {
      cursor: pointer;
    }

    .status-pill {
      display: inline-block;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 0.875rem;
      background: #eaf2ff;
      color: #1f4e9f;
    }
  </style>
</head>
<body>
  <main class="app-shell">
    <section class="mb-4">
      <h1 class="h3 mb-1">Eventos</h1>
      <p class="text-muted mb-0">Cliente demo en PHP + jQuery para consumir la API de eventos.</p>
    </section>

    <section class="card card-soft mb-4">
      <div class="card-body">
        <form id="filtersForm" class="row g-3 align-items-end">
          <div class="col-12 col-md-3">
            <label class="form-label" for="fromDate">Desde</label>
            <input id="fromDate" class="form-control" type="date" />
          </div>
          <div class="col-12 col-md-3">
            <label class="form-label" for="toDate">Hasta</label>
            <input id="toDate" class="form-control" type="date" />
          </div>
          <div class="col-12 col-md-2">
            <label class="form-label" for="pageSize">Tamano</label>
            <select id="pageSize" class="form-select">
              <option value="10" selected>10</option>
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
          <div class="col-12 col-md-4 d-flex gap-2">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <button type="button" id="resetFilters" class="btn btn-outline-secondary">Limpiar</button>
          </div>
        </form>
      </div>
    </section>

    <section class="card card-soft">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <span id="statusPill" class="status-pill">Listo</span>
          <strong id="resultMeta" class="text-muted">Total: 0</strong>
        </div>

        <div id="alertBox" class="alert alert-danger d-none" role="alert"></div>

        <div class="table-wrap border rounded">
          <table class="table table-hover mb-0 align-middle">
            <thead class="table-light sticky-top">
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

        <div class="d-flex justify-content-between align-items-center mt-3">
          <button id="prevPage" class="btn btn-outline-primary" type="button">Anterior</button>
          <span id="pageInfo" class="text-muted">Pagina 1</span>
          <button id="nextPage" class="btn btn-outline-primary" type="button">Siguiente</button>
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
      statusPill.removeClass('bg-danger-subtle text-danger bg-success-subtle text-success');

      if (tone === 'error') {
        statusPill.addClass('bg-danger-subtle text-danger');
      } else if (tone === 'success') {
        statusPill.addClass('bg-success-subtle text-success');
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
        const detailBtn = $('<button type="button" class="btn btn-sm btn-outline-primary">Ver detalle</button>');
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
      $('#filtersForm').on('submit', function (event) {
        event.preventDefault();
        state.from = String($('#fromDate').val() || '');
        state.to = String($('#toDate').val() || '');
        state.size = Number($('#pageSize').val() || 10);
        state.page = 1;
        loadEvents();
      });

      $('#resetFilters').on('click', function () {
        $('#fromDate').val('');
        $('#toDate').val('');
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
