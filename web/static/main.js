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
document.getElementById('budget-form').addEventListener('submit', async (e) => {
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
document.getElementById('predict-form').addEventListener('submit', async (e) => {
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
