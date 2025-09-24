document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('btn-generar-form');
    if (!btn) return;
    btn.addEventListener('click', async function() {
        // Cargar el JSON de plantilla
        const response = await fetch('/static/plantilla.json');
        const data = await response.json();
        const fields = data.fields || [];
        const form = document.createElement('form');
        form.setAttribute('id', 'formulario-dinamico');
        fields.forEach(field => {
            const div = document.createElement('div');
            div.className = 'mb-3';
            const label = document.createElement('label');
            label.textContent = field.label;
            label.setAttribute('for', field.id);
            div.appendChild(label);
            let input;
            if (field.type === 'select') {
                input = document.createElement('select');
                input.className = 'form-select';
                input.id = field.id;
                input.name = field.id;
                // Opciones desde catálogo
                if (data.catalogs && field.options_catalog && data.catalogs[field.options_catalog]) {
                    data.catalogs[field.options_catalog].forEach(opt => {
                        const option = document.createElement('option');
                        option.value = opt;
                        option.textContent = opt;
                        input.appendChild(option);
                    });
                }
            } else if (field.type === 'file' || field.type === 'signature') {
                input = document.createElement('input');
                input.type = 'file';
                input.className = 'form-control';
                input.id = field.id;
                input.name = field.id;
            } else {
                input = document.createElement('input');
                input.type = field.type === 'number' ? 'number' : 'text';
                input.className = 'form-control';
                input.id = field.id;
                input.name = field.id;
                if (field.placeholder) input.placeholder = field.placeholder;
            }
            div.appendChild(input);
            form.appendChild(div);
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
