// Mapa d'imatges locals verificades — web/static/img/
const CAR_IMAGES = {
    "volkswagen_golf":          "/static/img/vw_golf.jpg",
    "volkswagen_polo":          "/static/img/vw_polo.jpg",
    "volkswagen_passat":        "/static/img/vw_passat.jpg",
    "volkswagen_passatvariant": "/static/img/vw_passat.jpg",
    "volkswagen_tiguan":        "/static/img/vw_tiguan.jpg",
    "volkswagen_touran":        "/static/img/vw_touran.jpg",
    "audi_a3":                  "/static/img/audi_a3.jpg",
    "audi_a4":                  "/static/img/audi_a4.jpg",
    "audi_a5":                  "/static/img/audi_a5.jpg",
    "audi_a6":                  "/static/img/audi_a6.jpg",
    "audi_q5":                  "/static/img/audi_q5.jpg",
    "bmw_116":                  "/static/img/bmw_116.jpg",
    "bmw_118":                  "/static/img/bmw_118.jpg",
    "bmw_316":                  "/static/img/bmw_318.jpg",
    "bmw_318":                  "/static/img/bmw_318.jpg",
    "bmw_320":                  "/static/img/bmw_320.jpg",
    "bmw_x1":                   "/static/img/bmw_x1.jpg",
    "bmw_x3":                   "/static/img/bmw_x3.jpg",
    "bmw_x5":                   "/static/img/bmw_x5.jpg",
    "mercedes-benz_c220":       "/static/img/mb_c220.jpg",
    "mercedes-benz_a180":       "/static/img/mb_a180.jpg",
    "mercedes-benz_e220":       "/static/img/mb_e220.jpg",
    "seat_leon":                "/static/img/seat_leon.jpg",
    "seat_ibiza":               "/static/img/seat_ibiza.jpg",
    "seat_arona":               "/static/img/seat_arona.jpg",
};

const MAKE_EMOJI = {
    bmw: '🏎️', "mercedes-benz": '⭐', audi: '💎', porsche: '🏁',
    volkswagen: '🚗', seat: '🚙', renault: '🔵', peugeot: '🦁',
    citroen: '🚗', ford: '🔵', toyota: '🇯🇵', honda: '🚗',
    tesla: '⚡', volvo: '🇸🇪', hyundai: '🇰🇷', kia: '🇰🇷',
    nissan: '🇯🇵', mazda: '🇯🇵', fiat: '🇮🇹', opel: '⚡',
    skoda: '🇨🇿', dacia: '🚗', mini: '🇬🇧', default: '🚗'
};

function getImageKey(make, model) {
    return `${make.toLowerCase()}_${model.toLowerCase().replace(/\s+/g, '_')}`;
}

function getCarImage(make, model) {
    const key = getImageKey(make, model);
    return CAR_IMAGES[key] || null;
}

function getFallbackEmoji(make) {
    return MAKE_EMOJI[make.toLowerCase()] || MAKE_EMOJI.default;
}

function showEmoji(thumbEl, make, badge) {
    const emoji = document.createElement('span');
    emoji.className = 'car-emoji';
    emoji.textContent = getFallbackEmoji(make);
    thumbEl.insertBefore(emoji, badge);
}

function setThumbImage(thumbEl, src, make) {
    const badge = thumbEl.querySelector('.car-fuel-badge, .moto-type-badge');
    thumbEl.innerHTML = '';
    if (badge) thumbEl.appendChild(badge);

    if (src) {
        const img = document.createElement('img');
        img.src = src;
        img.alt = make;
        img.className = 'car-img';
        img.onerror = () => { img.remove(); showEmoji(thumbEl, make, badge); };
        thumbEl.insertBefore(img, badge);
    } else {
        showEmoji(thumbEl, make, badge);
    }
}

function loadCarImages() {
    const cards = document.querySelectorAll('.car-card, .moto-card');
    cards.forEach(card => {
        const make = card.dataset.make;
        const model = card.dataset.model;
        const thumbEl = card.querySelector('.car-thumb, .moto-thumb');
        if (!thumbEl) return;
        const src = getCarImage(make, model);
        setThumbImage(thumbEl, src, make);
    });
}

document.addEventListener('DOMContentLoaded', loadCarImages);
