var FingerprintSdkTest = (function () { 
	function FingerprintSdkTest() {
		this.sdk = new Fingerprint.WebApi; 
	}
FingerprintSdkTest.prototype.getDeviceList = function () { 	
		return this.sdk.enumerateDevices();
	};
	return FingerprintSdkTest; 
})();

window.onload = function () {
	test = new FingerprintSdkTest();
	var allReaders = test.getDeviceList();
		allReaders.then(function (sucessObj) { 
			for (i=0;i<sucessObj.length;i++){
				console.log(sucessObj[i]); 
			}
	}, function (error){ 
			console.log(error.message);
	}); 
}
