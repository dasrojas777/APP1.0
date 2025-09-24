document.addEventListener('DOMContentLoaded', async function() {
    // Cargar protocolos.json y poblar el menú

    const select = document.getElementById('select-protocolo');
    const btn = document.getElementById('btn-generar-form');
    let protocolos = [];
    let protocoloSeleccionado = null;
    let catalogosGlobal = {};
    try {
        const response = await fetch('/static/protocolos.json');
        const data = await response.json();
        protocolos = data.protocolos || [];
        catalogosGlobal = data.catalogos || {};
        window.protocolosCatalogosGlobal = catalogosGlobal;
        select.innerHTML = '';
        const defaultOpt = document.createElement('option');
        defaultOpt.value = '';
        defaultOpt.selected = true;
        defaultOpt.disabled = true;
        defaultOpt.textContent = 'Selecciona un protocolo';
        select.appendChild(defaultOpt);
        if (protocolos && protocolos.length > 0) {
            protocolos.forEach((p, idx) => {
                const opt = document.createElement('option');
                opt.value = idx;
                opt.textContent = p.tipo_protocolo;
                select.appendChild(opt);
            });
        }
    } catch (e) {
        select.innerHTML = '<option value="" selected>Error cargando protocolos</option>';
    }

    select.addEventListener('change', function() {
        const idx = parseInt(select.value);
        protocoloSeleccionado = protocolos[idx];
        btn.disabled = isNaN(idx) || !protocoloSeleccionado;
    });

    btn.addEventListener('click', function() {
        if (!protocoloSeleccionado) return;
        const form = document.createElement('form');
        form.setAttribute('id', 'formulario-dinamico');
        // Clase única por tipo_protocolo (slug)
        const slug = protocoloSeleccionado.tipo_protocolo
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/(^-|-$)/g, '');
        form.classList.add('formulario-' + slug);
        // Catálogos: primero del protocolo, si no, del objeto raíz
        const catalogos = protocoloSeleccionado.catalogos || window.protocolosCatalogosGlobal || catalogosGlobal || {};
        const estructura = protocoloSeleccionado.estructura || [];

        function renderCampo(campo, parentName) {
            if (campo.tipo === 'grupo' && Array.isArray(campo.subcampos)) {
                const nombres = campo.subcampos.map(sc => sc.nombre && sc.nombre.toLowerCase());
                const groupDiv = document.createElement('div');
                groupDiv.className = 'mb-3';
                // Título siempre arriba
                if (campo.nombre) {
                    const groupLabel = document.createElement('label');
                    groupLabel.textContent = campo.nombre;
                    groupLabel.className = 'fw-bold d-block';
                    groupDiv.appendChild(groupLabel);
                }
                // Si existen ambos 'Desde' y 'Hasta', mostrar primero 'Eje (cara)' si existe, luego la fila 'Desde' y 'Hasta', luego el resto
                if (nombres.includes('desde') && nombres.includes('hasta')) {
                    // Mostrar primero 'Eje (cara)' si existe
                    const ejeCara = campo.subcampos.find(sc => sc.nombre && sc.nombre.toLowerCase().includes('eje'));
                    if (ejeCara) {
                        groupDiv.appendChild(renderCampo(ejeCara, campo.nombre));
                    }
                    // Fila 'Desde' y 'Hasta'
                    const row = document.createElement('div');
                    row.className = 'd-flex gap-2 grupo-desde-hasta';
                    ['desde','hasta'].forEach(nombre => {
                        const subcampo = campo.subcampos.find(sc => sc.nombre && sc.nombre.toLowerCase() === nombre);
                        if (subcampo) {
                            const div = document.createElement('div');
                            div.className = 'flex-fill';
                            const label = document.createElement('label');
                            label.textContent = subcampo.nombre;
                            label.className = 'form-label';
                            div.appendChild(label);
                            let input;
                            if (subcampo.tipo === 'numérico' || subcampo.tipo === 'numérico_con_unidad') {
                                input = document.createElement('input');
                                input.type = 'number';
                                input.className = 'form-control';
                            } else {
                                input = document.createElement('input');
                                input.type = 'text';
                                input.className = 'form-control';
                            }
                            div.appendChild(input);
                            row.appendChild(div);
                        }
                    });
                    groupDiv.appendChild(row);
                    // Renderizar el resto de subcampos debajo de la fila
                    campo.subcampos.forEach(subcampo => {
                        const nombre = subcampo.nombre && subcampo.nombre.toLowerCase();
                        if (nombre !== 'desde' && nombre !== 'hasta' && !(subcampo.nombre && subcampo.nombre.toLowerCase().includes('eje'))) {
                            groupDiv.appendChild(renderCampo(subcampo, campo.nombre));
                        }
                    });
                } else {
                    campo.subcampos.forEach(subcampo => {
                        groupDiv.appendChild(renderCampo(subcampo, campo.nombre));
                    });
                }
                return groupDiv;
            } else {
                const div = document.createElement('div');
                div.className = 'mb-3';
                const label = document.createElement('label');
                label.textContent = campo.nombre;
                div.appendChild(label);
                let input;
                if (campo.tipo === 'seleccion_unica' && campo.catalogo) {
                    input = document.createElement('select');
                    input.className = 'form-select';
                    const opciones = catalogos[campo.catalogo] || [];
                    opciones.forEach(opt => {
                        const option = document.createElement('option');
                        option.value = opt;
                        option.textContent = opt;
                        input.appendChild(option);
                    });
                } else if (campo.tipo === 'numérico' || campo.tipo === 'numérico_con_unidad') {
                    if (campo.tipo === 'numérico_con_unidad' && campo.catalogo_unidad) {
                        // Input y select alineados horizontalmente
                        const row = document.createElement('div');
                        row.className = 'd-flex gap-2 grupo-num-unidad';
                        input = document.createElement('input');
                        input.type = 'number';
                        input.className = 'form-control';
                        const selectUnidad = document.createElement('select');
                        selectUnidad.className = 'form-select';
                        (catalogos[campo.catalogo_unidad] || []).forEach(opt => {
                            const option = document.createElement('option');
                            option.value = opt;
                            option.textContent = opt;
                            selectUnidad.appendChild(option);
                        });
                        row.appendChild(input);
                        row.appendChild(selectUnidad);
                        div.appendChild(row);
                        return div;
                    } else {
                        input = document.createElement('input');
                        input.type = 'number';
                        input.className = 'form-control';
                    }
                } else if (campo.tipo === 'texto') {
                    input = document.createElement('input');
                    input.type = 'text';
                    input.className = 'form-control';
                } else {
                    input = document.createElement('input');
                    input.type = 'text';
                    input.className = 'form-control';
                }
                div.appendChild(input);
                return div;
            }
        }

        estructura.forEach(seccion => {
            // Título de sección
            if (seccion.seccion) {
                const h4 = document.createElement('h4');
                h4.textContent = seccion.seccion;
                h4.className = 'mt-4 mb-3';
                form.appendChild(h4);
            }
            // Campos directos
            if (seccion.campos) {
                seccion.campos.forEach(campo => {
                    form.appendChild(renderCampo(campo));
                });
            }
            // Subsecciones
            if (seccion.subsecciones) {
                seccion.subsecciones.forEach(subsec => {
                    if (subsec.subtitulo) {
                        const h5 = document.createElement('h5');
                        h5.textContent = subsec.subtitulo;
                        h5.className = 'mb-2';
                        form.appendChild(h5);
                    }
                    if (subsec.campos) {
                        subsec.campos.forEach(campo => {
                            form.appendChild(renderCampo(campo));
                        });
                    }
                });
            }
        });
        // Botón de envío
        const submit = document.createElement('button');
        submit.type = 'submit';
        submit.className = 'btn btn-success w-100';
        submit.textContent = 'Enviar';
        form.appendChild(submit);
        // Insertar el formulario en el placeholder
        const placeholder = document.getElementById('formulario-dinamico-placeholder');
        placeholder.innerHTML = '';
        placeholder.appendChild(form);
    });
});
