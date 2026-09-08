/* Consent-Banner (vanilla-cookieconsent v3) + Google Consent Mode v2
   Selbst gehostet, kein Vendor-Dashboard. Kategorien: necessary, analytics (GA4), marketing (Meta). */
(function () {
  var pixelPushed = false;
  function updateConsent () {
    var a = CookieConsent.acceptedCategory('analytics');
    var m = CookieConsent.acceptedCategory('marketing');
    gtag('consent', 'update', {
      analytics_storage: a ? 'granted' : 'denied',
      ad_storage:        m ? 'granted' : 'denied',
      ad_user_data:      m ? 'granted' : 'denied',
      ad_personalization:m ? 'granted' : 'denied'
    });
    // Meta Pixel erst bei Marketing-Einwilligung und genau einmal pro Seite auslösen
    window.dataLayer = window.dataLayer || [];
    if (m && !pixelPushed) {
      pixelPushed = true;
      window.dataLayer.push({ event: 'cookie_consent_update' });
    }
  }
  CookieConsent.run({
    guiOptions: {
      consentModal: { layout: 'box inline', position: 'bottom left' },
      preferencesModal: { layout: 'box' }
    },
    categories: {
      necessary: { readOnly: true, enabled: true },
      analytics: {},
      marketing: {}
    },
    onFirstConsent: updateConsent,
    onConsent: updateConsent,
    onChange: updateConsent,
    language: {
      default: 'de',
      translations: {
        de: {
          consentModal: {
            title: 'Wir respektieren deine Privatsphäre',
            description: 'Diese Website nutzt Cookies und ähnliche Technologien für Statistik (Google Analytics) und Marketing (Meta) — nur mit deiner Einwilligung. Notwendige Cookies sind für den Betrieb erforderlich.',
            acceptAllBtn: 'Alle akzeptieren',
            acceptNecessaryBtn: 'Nur notwendige',
            showPreferencesBtn: 'Einstellungen',
            footer: '<a href="datenschutz.html">Datenschutz</a> · <a href="impressum.html">Impressum</a>'
          },
          preferencesModal: {
            title: 'Cookie-Einstellungen',
            acceptAllBtn: 'Alle akzeptieren',
            acceptNecessaryBtn: 'Nur notwendige',
            savePreferencesBtn: 'Auswahl speichern',
            closeIconLabel: 'Schließen',
            sections: [
              { title: 'Verwendung von Cookies', description: 'Du entscheidest, welche Kategorien du zulässt. Deine Auswahl kannst du jederzeit über „Cookie-Einstellungen" im Footer ändern.' },
              { title: 'Notwendig', description: 'Für den Betrieb der Website erforderlich. Immer aktiv.', linkedCategory: 'necessary' },
              { title: 'Statistik — Google Analytics', description: 'Anonyme Reichweiten- und Nutzungsmessung (GA4), um die Website zu verbessern.', linkedCategory: 'analytics' },
              { title: 'Marketing — Meta', description: 'Meta Pixel / Conversions API zur Messung und Optimierung von Werbung.', linkedCategory: 'marketing' },
              { title: 'Mehr Informationen', description: 'Details in der <a href="datenschutz.html">Datenschutzerklärung</a>.' }
            ]
          }
        }
      }
    }
  });
})();
