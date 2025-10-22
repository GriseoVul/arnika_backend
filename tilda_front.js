window.t_onReadyFunctions = window.t_onReadyFunctions || [];
window.t_onReadyFunctions.push(init);

if (document.readyState !== 'loading') {
  init();
} else {
  document.addEventListener('DOMContentLoaded', init);
}
const API_URL = "https://api.odaa.studio/api/data";
  /* колонка Google Sheets → CSS-класс */
const MAP = {
  // паспорт аптеки
  'Название': '.ph-title',
  'Статус': '.ph-status',
  'Номер аптеки по лицензии': '.ph-licence',
  'Город': '.ph-city',
  'Район': '.ph-district',
  'Адрес': '.ph-address',
  'Номер телефона': '.ph-phone',
  'Ориентир': '.ph-landmark',

  // график
  'ПН': '.ph-mon', 'ВТ': '.ph-tue', 'СР': '.ph-wed', 'ЧТ': '.ph-thu',
  'ПТ': '.ph-fri', 'СБ': '.ph-sat', 'ВС': '.ph-sun',

  // акции / вакансии
  'Акция1': '.ph-sale1', 'Акция2': '.ph-sale2',
  'Вакансия1': '.ph-job1', 'Вакансия2': '.ph-job2'
};

function put(selector, value) {
  const element = document.querySelector(selector);

  if (!element) {
    console.warn(`element ${selector} not found`);
    return;
  }

  if (value === undefined || value === null || value === '') {
    return;
  }

  if (selector === '.ph-map-link' && value) {
    element.href = value;
    return;
  }

  if (selector === '.ph-phone' && value) {
    const cleanPhone = String(value).replace(/\D/g, '');
    element.href = `tel:${cleanPhone}`;
  }
  element.textContent = value;
}

async function getData() {
  const slug = window.location.pathname.split('/').pop();
  const response = await fetch(`${API_URL}/${slug}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

async function init() {
  try {
    const slug = window.location.pathname.split('/').pop();

    if (!slug) {
      console.warn(`[apteki] slug "${slug}" не найден`);
      return;
    }

    const row = await getData();
    Object.entries(MAP).forEach(([col, cls]) => put(cls, row[col]));

  } catch (e) {
    console.error('[apteki] load error', e);
    // показываем fallback-сообщение
    put('.ph-title', '⚠️ Нет соединения с сервером');
  }
}