var lightBoxDoamin;
(function () {
    window.Lightbox = window.Lightbox || {};
    Lightbox.Checkout = (function () {
        var configure = {};
        function showLightbox() {

            if (this.configure) {

                var urlsrc = GetLightBoxUrl(this.configure,false,false);

                var ifrm = document.createElement("iframe");
                ifrm.id = "Lightbox";
                ifrm.setAttribute("src", urlsrc);
                ifrm.style.zIndex = "999999";
                ifrm.style.display = "block";
                ifrm.style.backgroundColor = "transparent";
                ifrm.style.border = "0px none transparent";
                ifrm.style.overflowX = "hidden"; //hidden
                ifrm.style.overflowY = "auto"; //scroll//auto

                ifrm.style.visibility = "visible";
                ifrm.style.margin = "0px";
                ifrm.style.padding = "0px";
                ifrm.style.position = "fixed";
                ifrm.style.left = "0px";
                ifrm.style.top = "0px;"
                ifrm.style.bottom = "0px";
                ifrm.style.right = "0px";
                ifrm.style.width = "100%";
                ifrm.style.height = "100%";
                document.body.appendChild(ifrm);


                window.addEventListener('message', function (event) {
                    var parser = document.createElement('a');
                    parser.href = lightBoxDoamin;
					var ua= window.navigator.userAgent;

                    if (event.origin === parser.origin || (parser.origin == undefined && (ua.indexOf('MSIE ') > 0|| ua.indexOf('Trident/')>0 || ua.indexOf('Edge/')>0))) {
                        if (event.data != null && event.data != '') {

                            if (event.data.callback == 'errorCallback' && this.Lightbox.Checkout.configure.errorCallback !== undefined) {
                                this.Lightbox.Checkout.configure.errorCallback(event.data.Info);
                            }
                            else if (event.data.callback == 'completeCallback' && this.Lightbox.Checkout.configure.completeCallback !== undefined) {
                                this.Lightbox.Checkout.configure.completeCallback(event.data.paymentInfo);
                            }
                            else if (event.data.callback == 'cancelCallback'){

								closeLightbox();

								if(this.Lightbox.Checkout.configure.cancelCallback !== undefined) {
									this.Lightbox.Checkout.configure.cancelCallback();
								}
							}
                        }
                    }
                }, false);

            } else {
                console.log('no configuration');
            }
        };

		function closeLightbox(){

			var elem = document.getElementById('Lightbox');
                        if (elem != null && elem.parentNode != null) {
                            elem.parentNode.removeChild(elem);
                        }
		};



        function showPaymentPage() {
            if (this.configure) {
                window.location =GetLightBoxUrl(this.configure,true,true);

            } else {
                console.log('no configuration');
            }
        };



        function GetLightBoxUrl(configure,hideCloseButton,isEnableReturnUrl){

			if (configure) {
				lightBoxDoamin = 'https://npg.moamalat.net:6006/'; //'http://www.testsite.com:3629/';//'https://upg.egyptianbanks.com:3008/PayInterface';


                var paymentMethodFromLightBox = null;
                var mId = 0;
                var tId = 0;
                var orderId = "";
                var amount = 0;
				var feeAmount=0;
                var MerchantReference = "";
		var returnUrl="";
                var configPath = window.Lightbox.Checkout.configure;
		var  secureHash = "";
		var  trxDateTime = "";
		var ExpirationDateTime = "";

		var customerEmail ='';
        var customerMobile ='';
        var messageCustomer='';
        var merchantCustomerId ='';
        var currencyTwo='';
        var currencyTwoValue='';
        var additionalFees=0;

		var showCustomerEmail=null;
		var showCustomerMobile=null;
		var showMessageCustomer=null;
		var showMerchantCustomerId=null;
		var showCurrencyTwo=null;
		var showAdditionalFees=null;
		var consumerEnterAmount=null;


	   var topBarColor =null;
       var buttonPayColor =null;
       var bodyBackgroundColor =null;
       var textcolor =null;
       var linkTextColor =null;
       var scrollbarColor =null;
       var scrollbarBackgroundColor =null;
       var paymentInfoBackgroundColor =null;
       var paymentInfoLineColor =null;
       var headerOrFooterLineColor =null;
       var closeButtonColor =null;
       var closeButtonBackgroundColor =null;
       var logoOne  ='';
	   var invoiceNo='';
       var invoiceServicesStr='';
	   var feeAmount=null;

                if (typeof (configPath.paymentMethodFromLightBox) !== 'undefined') {
                    paymentMethodFromLightBox = configPath.paymentMethodFromLightBox;
                }

                if (typeof (configPath.OrderId) !== 'undefined' && configPath.OrderId !== null) {
                    orderId = configPath.OrderId;

                }
                if (typeof (configPath.MID) !== 'undefined' && configPath.MID !== null && !isNaN(configPath.MID)) {
                    mId = configPath.MID;
                }
                if (typeof (configPath.TID) !== 'undefined' && configPath.TID !== null && !isNaN(configPath.TID)) {
                    tId = configPath.TID;
                }

                if (typeof (configPath.AmountTrxn) !== 'undefined' && configPath.AmountTrxn !== null && !isNaN(configPath.AmountTrxn)) {
                    amount = configPath.AmountTrxn / 1000;
                }
                if (typeof (configPath.MerchantReference) !== 'undefined' && configPath.MerchantReference !== null) {
                    MerchantReference = configPath.MerchantReference;
                }

                if (typeof (configPath.ReturnUrl) !== 'undefined' && configPath.ReturnUrl !== null) {
                    returnUrl = configPath.ReturnUrl;
                }
				 if (typeof (configPath.SecureHash) !== 'undefined') {
                    secureHash = configPath.SecureHash;
                }

		        if (typeof (configPath.TrxDateTime) !== 'undefined') {
                    trxDateTime = configPath.TrxDateTime;
                }

		        if (typeof (configPath.ExpirationDateTime) !== 'undefined') {
                    ExpirationDateTime = configPath.ExpirationDateTime;
                }

				 if (typeof (configPath.InvoiceNo) !== 'undefined') {
                    invoiceNo = configPath.InvoiceNo;
                }

				 if (typeof (configPath.InvoiceServicesStr) !== 'undefined') {
                    invoiceServicesStr = configPath.InvoiceServicesStr;
                }

				 if (typeof (configPath.FeeAmount) !== 'undefined' && configPath.FeeAmount !== null && !isNaN(configPath.FeeAmount)) {
                    feeAmount = configPath.FeeAmount / 1000;
                }

            if (typeof (configPath.AdditionalCustomerData) !== 'undefined' && configPath.AdditionalCustomerData !== null) {
                if (typeof (configPath.AdditionalCustomerData.CustomerEmail) !== 'undefined' && configPath.AdditionalCustomerData.CustomerEmail !== null) {
                    customerEmail = configPath.AdditionalCustomerData.CustomerEmail;
                }
				if (typeof (configPath.AdditionalCustomerData.CustomerMobile) !== 'undefined' && configPath.AdditionalCustomerData.CustomerMobile !== null) {
                    customerMobile = configPath.AdditionalCustomerData.CustomerMobile;
                }
				if (typeof (configPath.AdditionalCustomerData.MessageCustomer) !== 'undefined' && configPath.AdditionalCustomerData.MessageCustomer !== null) {
                    messageCustomer = configPath.AdditionalCustomerData.MessageCustomer;
                }
				if (typeof (configPath.AdditionalCustomerData.MerchantCustomerId) !== 'undefined' && configPath.AdditionalCustomerData.MerchantCustomerId !== null) {
                    merchantCustomerId = configPath.AdditionalCustomerData.MerchantCustomerId;
                }
				if (typeof (configPath.AdditionalCustomerData.CurrencyTwo) !== 'undefined' && configPath.AdditionalCustomerData.CurrencyTwo !== null) {
                    currencyTwo = configPath.AdditionalCustomerData.CurrencyTwo;
                }

				if (typeof (configPath.AdditionalCustomerData.CurrencyTwoValue) !== 'undefined' && configPath.AdditionalCustomerData.CurrencyTwoValue !== null) {
                    currencyTwoValue = configPath.AdditionalCustomerData.CurrencyTwoValue;
                }

				if (typeof (configPath.AdditionalCustomerData.AdditionalFees) !== 'undefined' && configPath.AdditionalCustomerData.AdditionalFees !== null &&  !isNaN(configPath.AdditionalCustomerData.AdditionalFees)) {
                    additionalFees = configPath.AdditionalCustomerData.AdditionalFees;
                }


				if (typeof (configPath.AdditionalCustomerData.ShowCustomerEmail) !== 'undefined' && configPath.AdditionalCustomerData.ShowCustomerEmail !== null) {
                    showCustomerEmail = configPath.AdditionalCustomerData.ShowCustomerEmail;
                 }


				 if (typeof (configPath.AdditionalCustomerData.ShowCustomerMobile) !== 'undefined' && configPath.AdditionalCustomerData.ShowCustomerMobile !== null) {
                    showCustomerMobile = configPath.AdditionalCustomerData.ShowCustomerMobile;
                 }


				 if (typeof (configPath.AdditionalCustomerData.ShowMessageCustomer) !== 'undefined' && configPath.AdditionalCustomerData.ShowMessageCustomer !== null) {
                    showMessageCustomer = configPath.AdditionalCustomerData.ShowMessageCustomer;
                 }


				 if (typeof (configPath.AdditionalCustomerData.ShowMerchantCustomerId) !== 'undefined' && configPath.AdditionalCustomerData.ShowMerchantCustomerId !== null) {
                    showMerchantCustomerId = configPath.AdditionalCustomerData.ShowMerchantCustomerId;
                 }

				 if (typeof (configPath.AdditionalCustomerData.ShowCurrencyTwo) !== 'undefined' && configPath.AdditionalCustomerData.ShowCurrencyTwo !== null) {
                    showCurrencyTwo = configPath.AdditionalCustomerData.ShowCurrencyTwo;
                 }

				 if (typeof (configPath.AdditionalCustomerData.ShowAdditionalFees) !== 'undefined' && configPath.AdditionalCustomerData.ShowAdditionalFees !== null) {
                    showAdditionalFees = configPath.AdditionalCustomerData.ShowAdditionalFees;
                 }

				 	 if (typeof (configPath.AdditionalCustomerData.ConsumerEnterAmount) !== 'undefined' && configPath.AdditionalCustomerData.ConsumerEnterAmount !== null) {
                    consumerEnterAmount = configPath.AdditionalCustomerData.ConsumerEnterAmount;
                 }

			}

			if (typeof (configPath.LightBoxColorConfig) !== 'undefined' && configPath.LightBoxColorConfig !== null) {

                if (typeof (configPath.LightBoxColorConfig.TopBarColor) !== 'undefined' && configPath.LightBoxColorConfig.TopBarColor !== null) {
                    topBarColor = configPath.LightBoxColorConfig.TopBarColor;
                }

            if (typeof (configPath.LightBoxColorConfig.ButtonPayColor) !== 'undefined' && configPath.LightBoxColorConfig.ButtonPayColor !== null) {
                    buttonPayColor = configPath.LightBoxColorConfig.ButtonPayColor;
                }

   if (typeof (configPath.LightBoxColorConfig.BodyBackgroundColor) !== 'undefined' && configPath.LightBoxColorConfig.BodyBackgroundColor !== null) {
                    bodyBackgroundColor = configPath.LightBoxColorConfig.BodyBackgroundColor;
                }

        if (typeof (configPath.LightBoxColorConfig.Textcolor) !== 'undefined' && configPath.LightBoxColorConfig.Textcolor !== null) {
                    textcolor = configPath.LightBoxColorConfig.Textcolor;
                }


        if (typeof (configPath.LightBoxColorConfig.LinkTextColor) !== 'undefined' && configPath.LightBoxColorConfig.LinkTextColor !== null) {
                    linkTextColor = configPath.LightBoxColorConfig.LinkTextColor;
                }

              if (typeof (configPath.LightBoxColorConfig.ScrollbarColor) !== 'undefined' && configPath.LightBoxColorConfig.ScrollbarColor !== null) {
                    scrollbarColor = configPath.LightBoxColorConfig.ScrollbarColor;
                }

           if (typeof (configPath.LightBoxColorConfig.ScrollbarBackgroundColor) !== 'undefined' && configPath.LightBoxColorConfig.ScrollbarBackgroundColor !== null) {
                    scrollbarBackgroundColor = configPath.LightBoxColorConfig.ScrollbarBackgroundColor;
                }

			if (typeof (configPath.LightBoxColorConfig.PaymentInfoBackgroundColor) !== 'undefined' && configPath.LightBoxColorConfig.PaymentInfoBackgroundColor !== null) {
                    paymentInfoBackgroundColor = configPath.LightBoxColorConfig.PaymentInfoBackgroundColor;
                }

       		if (typeof (configPath.LightBoxColorConfig.PaymentInfoLineColor) !== 'undefined' && configPath.LightBoxColorConfig.PaymentInfoLineColor !== null) {
                    paymentInfoLineColor = configPath.LightBoxColorConfig.PaymentInfoLineColor;
                }

            if (typeof (configPath.LightBoxColorConfig.HeaderOrFooterLineColor) !== 'undefined' && configPath.LightBoxColorConfig.HeaderOrFooterLineColor !== null) {
                    headerOrFooterLineColor = configPath.LightBoxColorConfig.HeaderOrFooterLineColor;
                }

           if (typeof (configPath.LightBoxColorConfig.CloseButtonColor) !== 'undefined' && configPath.LightBoxColorConfig.CloseButtonColor !== null) {
                    closeButtonColor = configPath.LightBoxColorConfig.CloseButtonColor;
                }

           if (typeof (configPath.LightBoxColorConfig.CloseButtonBackgroundColor) !== 'undefined' && configPath.LightBoxColorConfig.CloseButtonBackgroundColor !== null) {
                    closeButtonBackgroundColor = configPath.LightBoxColorConfig.CloseButtonBackgroundColor;
                }

				   if (typeof (configPath.LightBoxColorConfig.LogoOne) !== 'undefined' && configPath.LightBoxColorConfig.LogoOne !== null) {
                    logoOne = configPath.LightBoxColorConfig.LogoOne;
                }
			}

                var lightboxHostedQueryString = '/?';
                lightboxHostedQueryString += 'paymentMethodFromLightBox=' + paymentMethodFromLightBox + '&';
                lightboxHostedQueryString += 'OrderID=' + orderId + '&';
                lightboxHostedQueryString += 'MID=' + mId + '&';
                lightboxHostedQueryString += 'MerchantReference=' + MerchantReference + '&';
                lightboxHostedQueryString += 'amount=' + amount + '&';
                lightboxHostedQueryString += 'TID=' + tId + '&';
		        lightboxHostedQueryString += 'secureHashAnonymous=' + secureHash + '&';
		        lightboxHostedQueryString += 'trxDateTime=' + trxDateTime + '&';
		        lightboxHostedQueryString += 'ExpirationDateTime=' + ExpirationDateTime + '&';

				lightboxHostedQueryString += 'CustomerEmail=' + customerEmail + '&';
				lightboxHostedQueryString += 'CustomerMobile=' + customerMobile + '&';
				lightboxHostedQueryString += 'MessageCustomer=' + messageCustomer + '&';
				lightboxHostedQueryString += 'MerchantCustomerId=' + merchantCustomerId + '&';
				lightboxHostedQueryString += 'CurrencyTwo=' + currencyTwo + '&';
				lightboxHostedQueryString += 'CurrencyTwoValue=' + currencyTwoValue + '&';
				lightboxHostedQueryString += 'AdditionalFees=' + additionalFees + '&';

				lightboxHostedQueryString += 'ShowCustomerEmail=' + showCustomerEmail + '&';
				lightboxHostedQueryString += 'ShowCustomerMobile=' + showCustomerMobile + '&';
				lightboxHostedQueryString += 'ShowMessageCustomer=' + showMessageCustomer + '&';
				lightboxHostedQueryString += 'ShowMerchantCustomerId=' + showMerchantCustomerId + '&';
				lightboxHostedQueryString += 'ShowCurrencyTwo=' + showCurrencyTwo + '&';
				lightboxHostedQueryString += 'ShowAdditionalFees=' + showAdditionalFees + '&';


				lightboxHostedQueryString += 'TopBarColor=' + topBarColor + '&';
				lightboxHostedQueryString += 'ButtonPayColor=' + buttonPayColor + '&';
				lightboxHostedQueryString += 'BodyBackgroundColor=' + bodyBackgroundColor + '&';
				lightboxHostedQueryString += 'Textcolor=' + textcolor + '&';
				lightboxHostedQueryString += 'LinkTextColor=' + linkTextColor + '&';
				lightboxHostedQueryString += 'ScrollbarColor=' + scrollbarColor + '&';
				lightboxHostedQueryString += 'ScrollbarBackgroundColor=' + scrollbarBackgroundColor + '&';
				lightboxHostedQueryString += 'PaymentInfoBackgroundColor=' + paymentInfoBackgroundColor + '&';
				lightboxHostedQueryString += 'PaymentInfoLineColor=' + paymentInfoLineColor + '&';
				lightboxHostedQueryString += 'HeaderOrFooterLineColor=' + headerOrFooterLineColor + '&';
				lightboxHostedQueryString += 'CloseButtonColor=' + closeButtonColor + '&';
				lightboxHostedQueryString += 'CloseButtonBackgroundColor=' + closeButtonBackgroundColor + '&';
				lightboxHostedQueryString += 'LogoOne=' + logoOne + '&';
				lightboxHostedQueryString += 'ConsumerEnterAmount=' + consumerEnterAmount + '&';
				lightboxHostedQueryString += 'invoiceNo=' + invoiceNo + '&';
				lightboxHostedQueryString += 'invoiceServicesStr=' + invoiceServicesStr + '&';
				lightboxHostedQueryString += 'feeAmount=' + feeAmount + '&';

		if(hideCloseButton){
		lightboxHostedQueryString += 'hideCloseButton=' + true + '&';
		if(isEnableReturnUrl){
		lightboxHostedQueryString += 'returnUrl=' + returnUrl;
		}
		}
                return lightBoxDoamin + '/Home/LightboxHostedCheckout' + lightboxHostedQueryString;
		}

		return "";
		}



  function getLightBoxUrl() {
            if (this.configure) {
               return GetLightBoxUrl(this.configure,true,false);

            } else {
               return "";
            }
        };


        // Public interface
        return {
            showLightbox: showLightbox,
			closeLightbox: closeLightbox,
            configure: configure,
			showPaymentPage:showPaymentPage,
			getLightBoxUrl:getLightBoxUrl
        };

    })();
})(window);