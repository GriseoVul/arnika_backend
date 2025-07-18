
(() => {
  /* ───────────── CONFIG ───────────── */
  const SHEET_ID   = '1fh-HOuPI_kNVrBgtv_Hf6DPHwe3l0bJs0pZYTS4Ul4o';
  const SHEET_TAB  = 'Аптеки';
  const CACHE_TTL  = 60 * 1000;                // 1 мин кэш в sessionStorage
  const FETCH_TIMEOUT = 7000;                  // 7 сек – отрубить «висящий» fetch
  const API_URL = "http://217.114.11.187:8000/api/data/"
  /* колонка Google Sheets → CSS-класс */
  const MAP = {
    // паспорт аптеки
    'Название'                : '.ph-title',
    'Статус'                  : '.ph-status',
    'Номер аптеки по лицензии': '.ph-licence',
    'Город'                   : '.ph-city',
    'Район'                   : '.ph-district',
    'Адрес'                   : '.ph-address',
    'Номер телефона'          : '.ph-phone',

    // график
    'ПН':'.ph-mon','ВТ':'.ph-tue','СР':'.ph-wed','ЧТ':'.ph-thu',
    'ПТ':'.ph-fri','СБ':'.ph-sat','ВС':'.ph-sun',

    // доп
    'Ориентир'        : '.ph-landmark',
    'График (бот)'    : '.ph-schedule-bot',
    'Карта всех аптек': '.ph-map-link',

    // акции / вакансии
    'Акция1':'.ph-sale1','Акция2':'.ph-sale2',
    'Вакансия1':'.ph-job1','Вакансия2':'.ph-job2'
  };

  function put(selector, value){
    const element = document.querySelector(selector);

    if(!element) {
        console.warn(`element ${selector} not found`);
        return ;
    }

    if(value === undefined || value === null || value === ''){
        // element.style.display = 'none';
        return ;
    }

    if ( selector === '.ph-map-link' && value) {
        element.href = value;
        // element.style.display = 'inline-block';
        return;
    }

    if (selector === '.ph-phone' && value) {
        const cleanPhone = value.replace(/\D/g, '')
        element.href = `tel:${cleanPhone}`
    }
    element.textContent = value;
    // element.style.display = ''
  }
  async function getData() {
    const slug = window.location.pathname.split('/').pop()
    const response = await fetch(`${API_URL}/${slug}`)
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
    }

    return [await response.json()];
  }
  (async () => {
    try {
      const slug = window.location.pathname.split('/').pop()

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
  })();
})();