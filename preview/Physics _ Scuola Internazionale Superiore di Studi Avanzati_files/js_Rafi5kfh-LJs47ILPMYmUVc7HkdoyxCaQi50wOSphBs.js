/*
 Copyright 2014 Google Inc. All rights reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 ---
 {as} Added language detection for Drupal sites.
 {as} Added sub-sites support.

 */

(function(window) {

  if (!!window.cookieChoices) {
    return window.cookieChoices;
  }

  var document = window.document;
  // IE8 does not support textContent, so we should fallback to innerText.
  var supportsTextContent = 'textContent' in document.body;

  var cookieChoices = (function() {

    var cookieNameBase = 'displayCookieConsent';
    var cookieConsentId = 'cookieChoiceInfo';
    var dismissLinkId = 'cookieChoiceDismiss';

    var cookieName = cookieNameBase;
    var cookiePath = "/";

    function setNameExt(extName) {
      cookieName = cookieNameBase + '-' + extName;
    }

    function setPath(thePath) {
      cookiePath = thePath;
    }

    function _createHeaderElement(cookieText, dismissText, linkText, linkHref) {
      var cookieConsentElement = document.createElement('div');
      cookieConsentElement.id = cookieConsentId;

      cookieConsentElement.appendChild(_createConsentText(cookieText));


	  var buttonContainer = document.createElement('div');
	  buttonContainer.className = 'cookie-buttons';
	  cookieConsentElement.appendChild(buttonContainer);

      var buttonPara = document.createElement('p');
      buttonContainer.appendChild(buttonPara);

      if (!!linkText && !!linkHref) {
        buttonPara.appendChild(_createInformationLink(linkText, linkHref));
      }
      buttonPara.appendChild(_createDismissLink(dismissText));
      return cookieConsentElement;
    }

    function _setElementText(element, text) {
      if (supportsTextContent) {
        element.textContent = text;
      } else {
        element.innerText = text;
      }
    }

    function _createConsentText(cookieText) {
      var consentContainer = document.createElement('div');
	  consentContainer.className = 'cookie-text';

      var consentPara = document.createElement('p');
      _setElementText(consentPara, cookieText);

	  consentContainer.appendChild(consentPara);
      return consentContainer;
    }

    function _createDismissLink(dismissText) {
      var dismissLink = document.createElement('a');
	  dismissLink.className = 'btn';
      _setElementText(dismissLink, dismissText);
      dismissLink.id = dismissLinkId;
      dismissLink.href = '#';
      return dismissLink;
    }

    function _createInformationLink(linkText, linkHref) {
      var infoLink = document.createElement('a');
	  infoLink.className = 'btn';
      _setElementText(infoLink, linkText);
      infoLink.href = linkHref;
      infoLink.target = '_blank';
      return infoLink;
    }

    function _dismissLinkClick() {
      _saveUserPreference();
      _removeCookieConsent();
      _httpGetPage();
      return false;
    }

    function _showCookieConsent(cookieText, dismissText, linkText, linkHref) {
      if (_shouldDisplayConsent()) {
        _removeCookieConsent();
        var consentElement = _createHeaderElement(cookieText, dismissText, linkText, linkHref);
        var fragment = document.createDocumentFragment();
        fragment.appendChild(consentElement);
        document.body.appendChild(fragment.cloneNode(true));
        document.getElementById(dismissLinkId).onclick = _dismissLinkClick;
      }
    }

    function showCookieConsentBar(cookieText, dismissText, linkText, linkHref) {
      _showCookieConsent(cookieText, dismissText, linkText, linkHref, false);
    }

    function _removeCookieConsent() {
      var cookieChoiceElement = document.getElementById(cookieConsentId);
      if (cookieChoiceElement != null) {
        cookieChoiceElement.parentNode.removeChild(cookieChoiceElement);
      }
    }

    function _saveUserPreference() {
      // Set the cookie expiry to one year after today.
      var expiryDate = new Date();
      expiryDate.setFullYear(expiryDate.getFullYear() + 1);
      document.cookie = 
	    cookieName + '=y;'
        + ' path=' + ((cookiePath.length) ? cookiePath : '/') + ';'
        + ' expires=' + expiryDate.toGMTString();
    }

    function _shouldDisplayConsent() {
      // Display the header only if the cookie has not been set.
      return !document.cookie.match(new RegExp(cookieName + '=([^;]+)'));
    }

    function _httpGetPage() {
      var url = window.location.href;
      if (url.indexOf('?') > -1){
        url += '&cookieconsent=yes&t=' + Math.random();
      }else{
        url += '?cookieconsent=yes&t=' + Math.random();
      }
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open( "GET", url, false );
      xmlHttp.send( null );
      return xmlHttp.responseText;
    }

    var exports = {};
    exports.showCookieConsentBar = showCookieConsentBar;
    exports.setNameExt = setNameExt;
    exports.setPath = setPath;
    return exports;
  })();

  window.cookieChoices = cookieChoices;
  return cookieChoices;
})(this);


/*
 * INIT
 */
jQuery(document).ready(function() {
	// Uncomment and set as required for subsites running on the same hostname
	// cookieChoices.setNameExt("XXXXsitename");
	// cookieChoices.setPath("/XXXXrootfolder");

	var currLang = jQuery('html').attr('xml:lang');
	if (!currLang) {
		currLang = jQuery('html').attr('lang');
	}
	switch (currLang) {
		case "it":
			cookieChoices.showCookieConsentBar("Su questo sito utilizziamo i cookie (anche di terze parti) per migliorare la tua esperienza utente. " 
				 +"Se prosegui nella navigazione del sito, ne acconsenti l’utilizzo.",
				 "OK",
				 "Maggiori informazioni...",
				 "/it/cookie-policy");
			break;
		default: /* en or missing */
			cookieChoices.showCookieConsentBar("We use cookies (including cookies from third parties) on this site to enhance your user experience. "
				+"By continuing to browse the site you are giving your consent for us to set cookies.",
				"OK",
				"More information...",
				"/cookie-policy");
	}
});

;
