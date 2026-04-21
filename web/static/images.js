const CAR_IMAGES = {
    // Volkswagen
    "volkswagen_golf":          "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/2020_Volkswagen_Golf_Style_1.5_Front.jpg/640px-2020_Volkswagen_Golf_Style_1.5_Front.jpg",
    "volkswagen_polo":          "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Volkswagen_Polo_VI_GTI_%282021%29_1X7A0344.jpg/640px-Volkswagen_Polo_VI_GTI_%282021%29_1X7A0344.jpg",
    "volkswagen_passat":        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Volkswagen_Passat_Variant_B9_IAA_2023_1X7A0654.jpg/640px-Volkswagen_Passat_Variant_B9_IAA_2023_1X7A0654.jpg",
    "volkswagen_passatvariant": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Volkswagen_Passat_Variant_B9_IAA_2023_1X7A0654.jpg/640px-Volkswagen_Passat_Variant_B9_IAA_2023_1X7A0654.jpg",
    "volkswagen_tiguan":        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Volkswagen_Tiguan_III_IMG_8388.jpg/640px-Volkswagen_Tiguan_III_IMG_8388.jpg",
    "volkswagen_touran":        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/2018_Volkswagen_Touran_1.6.jpg/640px-2018_Volkswagen_Touran_1.6.jpg",

    // Audi
    "audi_a3":                  "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Audi_A3_Allstreet_IMG_3202.jpg/640px-Audi_A3_Allstreet_IMG_3202.jpg",
    "audi_a4":                  "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Audi_A4_B9_sedans_%28FL%29_1X7A2441.jpg/640px-Audi_A4_B9_sedans_%28FL%29_1X7A2441.jpg",
    "audi_a5":                  "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Audi_A5_B10_DSC_7314.jpg/640px-Audi_A5_B10_DSC_7314.jpg",
    "audi_a6":                  "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Audi_A6_Avant_e-tron_DSC_7425.jpg/640px-Audi_A6_Avant_e-tron_DSC_7425.jpg",
    "audi_q5":                  "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Audi_Q5_Sportback_GU_DSC_9270.jpg/640px-Audi_Q5_Sportback_GU_DSC_9270.jpg",

    // BMW (116 usa la mateixa foto que 118 — de Wikimedia)
    "bmw_116":                  "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/BMW_118i%2C_BMW_Welt%2C_M%C3%BAnich%2C_Alemania05.JPG/640px-BMW_118i%2C_BMW_Welt%2C_M%C3%BAnich%2C_Alemania05.JPG",
    "bmw_118":                  "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/BMW_118i%2C_BMW_Welt%2C_M%C3%BAnich%2C_Alemania05.JPG/640px-BMW_118i%2C_BMW_Welt%2C_M%C3%BAnich%2C_Alemania05.JPG",
    "bmw_316":                  "https://upload.wikimedia.org/wikipedia/commons/b/bb/E21_BMW_316.jpg",
    "bmw_318":                  "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/1990_BMW_318_IS_Convertible.jpg/640px-1990_BMW_318_IS_Convertible.jpg",
    "bmw_320":                  "https://upload.wikimedia.org/wikipedia/commons/5/5c/BMW_320_I.JPG",
    "bmw_x1":                   "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/2018_BMW_X1_sDrive18i_xLine_1.5_Front.jpg/640px-2018_BMW_X1_sDrive18i_xLine_1.5_Front.jpg",
    "bmw_x3":                   "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/BMW_G45_X3_M50_DSC_7047.jpg/640px-BMW_G45_X3_M50_DSC_7047.jpg",
    "bmw_x5":                   "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/BMW_X5_M_%28G05%29_1X7A7047.jpg/640px-BMW_X5_M_%28G05%29_1X7A7047.jpg",

    // Mercedes-Benz
    "mercedes-benz_c220":       "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Mercedes-Benz_C220_Bluetec_diesel_%28W205%29_2143cc_registered_December_2014.jpg/640px-Mercedes-Benz_C220_Bluetec_diesel_%28W205%29_2143cc_registered_December_2014.jpg",
    "mercedes-benz_a180":       "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Mercedes-Benz_A180_%28W176%29_front.JPG/640px-Mercedes-Benz_A180_%28W176%29_front.JPG",
    "mercedes-benz_e220":       "https://upload.wikimedia.org/wikipedia/commons/a/a2/Mercedes-Benz_E220_CDi_T_S212_%288696606139%29.jpg",

    // Seat
    "seat_leon":                "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/2018_SEAT_Leon_FR_Technology_TSi_S-A_1.4_Front.jpg/640px-2018_SEAT_Leon_FR_Technology_TSi_S-A_1.4_Front.jpg",
    "seat_ibiza":               "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/2018_SEAT_Ibiza_SE_Technology_MPi_1.0_Front.jpg/640px-2018_SEAT_Ibiza_SE_Technology_MPi_1.0_Front.jpg",
    "seat_arona":               "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/2018_SEAT_Arona_SE_Technology_TSi_1.0_Front_%281%29.jpg/640px-2018_SEAT_Arona_SE_Technology_TSi_1.0_Front_%281%29.jpg",
};

const MAKE_EMOJI = {
    bmw: '🏎️', mercedes: '⭐', audi: '💎', porsche: '🏁',
    volkswagen: '🚗', seat: '🚙', renault: '🔵', peugeot: '🦁',
    citroen: '🚗', ford: '🔵', toyota: '🇯🇵', honda: '🚗',
    tesla: '⚡', volvo: '🇸🇪', hyundai: '🇰🇷', kia: '🇰🇷',
    nissan: '🇯🇵', mazda: '🇯🇵', fiat: '🇮🇹', opel: '⚡',
    skoda: '🇨🇿', dacia: '🚗', mini: '🇬🇧', default: '🚗'
};

const imageCache = {};

function getImageKey(make, model) {
    return `${make.toLowerCase()}_${model.toLowerCase().replace(/\s+/g, '_')}`;
}

async function fetchWikipediaPageImage(make, model) {
    const url = `https://en.wikipedia.org/w/api.php?` +
        `action=query&titles=${encodeURIComponent(make + ' ' + model)}` +
        `&prop=pageimages&piprop=thumbnail&pithumbsize=400` +
        `&format=json&origin=*`;
    try {
        const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
        const data = await res.json();
        const pages = Object.values(data?.query?.pages || {});
        return pages[0]?.thumbnail?.source || null;
    } catch (e) { return null; }
}

async function getCarImage(make, model) {
    const key = getImageKey(make, model);
    if (imageCache[key] !== undefined) return imageCache[key];

    // URL verificada → passar pel proxy del servidor
    if (CAR_IMAGES[key]) {
        const proxied = `/img-proxy?url=${encodeURIComponent(CAR_IMAGES[key])}`;
        imageCache[key] = proxied;
        return proxied;
    }

    // Fallback: pàgina Wikipedia
    const wikiSrc = await fetchWikipediaPageImage(make, model);
    imageCache[key] = wikiSrc ? `/img-proxy?url=${encodeURIComponent(wikiSrc)}` : null;
    return imageCache[key];
}

function getFallbackEmoji(make) {
    return MAKE_EMOJI[make.toLowerCase().split(' ')[0]] || MAKE_EMOJI.default;
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
        img.src = src; img.alt = make; img.className = 'car-img';
        img.onload = () => {
            if (img.naturalWidth / img.naturalHeight > 2.5) { img.remove(); showEmoji(thumbEl, make, badge); }
        };
        img.onerror = () => { img.remove(); showEmoji(thumbEl, make, badge); };
        thumbEl.insertBefore(img, badge);
    } else { showEmoji(thumbEl, make, badge); }
}

async function loadCarImages() {
    const cards = document.querySelectorAll('.car-card, .moto-card');
    const tasks = Array.from(cards).map(card => {
        const make = card.dataset.make;
        const model = card.dataset.model;
        const thumbEl = card.querySelector('.car-thumb, .moto-thumb');
        return async () => { setThumbImage(thumbEl, await getCarImage(make, model), make); };
    });
    const BATCH = 4;
    for (let i = 0; i < tasks.length; i += BATCH) {
        await Promise.all(tasks.slice(i, i + BATCH).map(t => t()));
    }
}

document.addEventListener('DOMContentLoaded', loadCarImages);
