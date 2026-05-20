// ── Modal motos ───────────────────────────────────────────
function obrirModal(nom, preu, urlMotosnet, urlMilanuncios, urlWallapop) {
    document.getElementById('modal-icon').textContent = '🏍️';
    document.getElementById('modal-title').textContent = nom;
    document.getElementById('modal-price').textContent = 'Preu orientatiu: ' + preu.replace(',', '.') + ' €';
    document.getElementById('modal-desc').textContent = 'Cerca aquesta moto a les principals plataformes de venda de segona mà a Espanya:';

    const lnkCoches = document.getElementById('link-coches');
    lnkCoches.href = urlMotosnet;
    document.getElementById('link-coches-name').textContent = 'Motos.net';
    document.getElementById('link-coches-desc').textContent = 'El portal líder de motos a Espanya';
    lnkCoches.querySelector('.modal-link-icon').textContent = '🏍️';

    document.getElementById('link-milanuncios').href = urlMilanuncios;
    document.getElementById('link-milanuncios').querySelector('.modal-link-icon').textContent = '🔍';
    document.getElementById('link-milanuncios').querySelector('.modal-link-name').textContent = 'Cerca a Google';
    document.getElementById('link-milanuncios').querySelector('.modal-link-desc').textContent = 'Resultats de Milanuncios, Vibbo i més';
    document.getElementById('link-wallapop').href = urlWallapop;

    // AutoScout24 per motos
    const queryAS = nom.replace(/ /g, '+');
    document.getElementById('link-autoscout').href = `https://www.autoscout24.es/lst?q=${queryAS}&vehc=M`;

    document.getElementById('modal-overlay').classList.add('visible');
    document.body.style.overflow = 'hidden';
}

function obrirModalBudget() {
    const pMin = document.getElementById('price_min').value;
    const pMax = document.getElementById('price_max').value;
    if (!pMin || !pMax) return;

    document.getElementById('modal-icon').textContent = '🚗';
    document.getElementById('modal-title').textContent = 'Cotxes entre ' + parseInt(pMin).toLocaleString('ca') + ' € i ' + parseInt(pMax).toLocaleString('ca') + ' €';
    document.getElementById('modal-price').textContent = 'Rang de preu aplicat als resultats de cerca';
    document.getElementById('modal-desc').textContent = 'Cerca cotxes en aquest rang de preu a les principals plataformes:';

    const lnkCoches = document.getElementById('link-coches');
    lnkCoches.href = `https://www.coches.net/segunda-mano/?precioDesde=${pMin}&precioHasta=${pMax}`;
    document.getElementById('link-coches-name').textContent = 'Coches.net';
    document.getElementById('link-coches-desc').textContent = 'El portal líder de cotxes a Espanya';
    lnkCoches.querySelector('.modal-link-icon').textContent = '🚗';

    document.getElementById('link-milanuncios').href =
        `https://www.milanuncios.com/coches-de-segunda-mano/?preciodesde=${pMin}&preciohasta=${pMax}`;
    document.getElementById('link-wallapop').href =
        `https://es.wallapop.com/app/search?keywords=cotxe&category_ids=100&min_sale_price=${pMin}&max_sale_price=${pMax}`;
    document.getElementById('link-autoscout').href =
        `https://www.autoscout24.es/lst?atype=C&pricefrom=${pMin}&priceto=${pMax}`;

    document.getElementById('modal-overlay').classList.add('visible');
    document.body.style.overflow = 'hidden';
}

function tancarModal() {
    document.getElementById('modal-overlay').classList.remove('visible');
    document.body.style.overflow = '';
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') tancarModal();
});

// ── Vehicle selector ──────────────────────────────────────
function selectVehicle(type) {
    const form = document.getElementById('predict-form');
    const motoMsg = document.getElementById('moto-msg');
    const resultCard = document.getElementById('result-card');
    const errorCard = document.getElementById('error-card');
    const btnCar = document.getElementById('btn-car');
    const btnMoto = document.getElementById('btn-moto');

    if (type === 'car') {
        form.style.display = 'block';
        motoMsg.classList.remove('visible');
        btnCar.classList.add('active');
        btnMoto.classList.remove('active');
    } else {
        form.style.display = 'none';
        motoMsg.classList.add('visible');
        btnMoto.classList.add('active');
        btnCar.classList.remove('active');
        resultCard.classList.remove('visible');
        errorCard.classList.remove('visible');
    }
}

// ── Theme toggle ──────────────────────────────────────────
const btn = document.getElementById('theme-toggle');
const icon = document.getElementById('toggle-icon');
const label = document.getElementById('toggle-label');

const savedTheme = localStorage.getItem('theme') || 'dark';
if (savedTheme === 'light') {
    document.body.classList.add('light');
    icon.textContent = '☀️';
    label.textContent = 'Mode clar';
}

btn.addEventListener('click', () => {
    const isLight = document.body.classList.toggle('light');
    icon.textContent = isLight ? '☀️' : '🌙';
    label.textContent = isLight ? 'Mode clar' : 'Mode fosc';
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
});

// ── Budget form ───────────────────────────────────────────
const budgetForm = document.getElementById('budget-form');
if (budgetForm) {
    budgetForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = document.getElementById('budget-btn');
    const resultDiv = document.getElementById('budget-result');
    const errorDiv = document.getElementById('budget-error');
    const btnText = btn.querySelector('.btn-text');

    resultDiv.classList.remove('visible');
    errorDiv.classList.remove('visible');
    btn.disabled = true;
    btnText.textContent = 'Cercant...';

    try {
        const formData = new FormData(e.target);
        const response = await fetch('/budget', { method: 'POST', body: formData });
        const data = await response.json();

        if (data.success) {
            document.getElementById('budget-count').textContent = data.count.toLocaleString('ca-ES');
            document.getElementById('budget-avg-price').textContent = data.avg_price.toLocaleString('ca-ES') + ' €';
            document.getElementById('budget-kms').textContent = data.avg_kms.toLocaleString('ca-ES') + ' km';
            document.getElementById('budget-months').textContent = data.avg_months + ' mesos';
            document.getElementById('budget-power').textContent = data.avg_power + ' CV';

            const makesEl = document.getElementById('budget-makes');
            makesEl.innerHTML = data.top_makes.map(m =>
                `<div class="budget-tag">${m.name} <span class="budget-tag-count">${m.count}</span></div>`
            ).join('');

            const fuelsEl = document.getElementById('budget-fuels');
            fuelsEl.innerHTML = data.top_fuels.map(f =>
                `<div class="budget-tag">${f.name} <span class="budget-tag-count">${f.count}</span></div>`
            ).join('');

            resultDiv.classList.add('visible');
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            document.getElementById('budget-error-msg').textContent = data.error;
            errorDiv.classList.add('visible');
        }
    } catch (err) {
        document.getElementById('budget-error-msg').textContent = 'Error de connexió.';
        errorDiv.classList.add('visible');
    } finally {
        btn.disabled = false;
        btnText.textContent = 'Cercar vehicles';
    }
});
}

const predictForm = document.getElementById('predict-form');
if (predictForm) {
    predictForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById('submit-btn');
    const resultCard = document.getElementById('result-card');
    const errorCard = document.getElementById('error-card');
    const resultPrice = document.getElementById('result-price');
    const btnText = submitBtn.querySelector('.btn-text');

    resultCard.classList.remove('visible');
    errorCard.classList.remove('visible');
    submitBtn.disabled = true;
    btnText.textContent = 'Calculant...';

    try {
        const formData = new FormData(e.target);

        // Valors per defecte per als camps opcionals
        if (!formData.get('months_old') || formData.get('months_old') === '') formData.set('months_old', '36');
        if (!formData.get('power')      || formData.get('power') === '')      formData.set('power', '110');
        if (!formData.get('kms')        || formData.get('kms') === '')        formData.set('kms', '50000');
        if (!formData.get('num_owners') || formData.get('num_owners') === '') formData.set('num_owners', '1');

        const response = await fetch('/predict', { method: 'POST', body: formData });
        const data = await response.json();

        if (data.success) {
            resultPrice.textContent = data.price_formatted;
            document.getElementById('price-low').textContent = data.price_low;
            document.getElementById('price-high').textContent = data.price_high;

            // Botó de cotxes similars
            const make = document.getElementById('make').value;
            const fuel = document.getElementById('fuel_type').value;
            const params = new URLSearchParams({
                make, fuel,
                price_low: data.price_low_raw,
                price_high: data.price_high_raw,
                predicted: data.price
            });
            document.getElementById('btn-similar').href = `/similar?${params}`;

            resultCard.classList.add('visible');
            resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            document.getElementById('error-msg').textContent = 'Error: ' + data.error;
            errorCard.classList.add('visible');
        }
    } catch (err) {
        document.getElementById('error-msg').textContent = 'Error de connexió. Comprova que el servidor està actiu.';
        errorCard.classList.add('visible');
    } finally {
        submitBtn.disabled = false;
        btnText.textContent = 'Calcular preu estimat';
    }
});
}