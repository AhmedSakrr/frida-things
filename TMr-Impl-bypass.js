Java.perform(function() {
    var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
    var java_arr = Java.use("java.util.ArrayList");
    // https://android.googlesource.com/platform/external/conscrypt/+/1186465/src/platform/java/org/conscrypt/TrustManagerImpl.java#391
    // checkTrustedRecursive(certs, host, clientAuth, untrustedChain, trustedChain, used);
    TrustManagerImpl.checkTrustedRecursive.implementation = function(arg1, arg2, arg3, arg4, arg5, arg6) {
        console.log('Bypassing TrustManagerImpl ..');
        var k = java_arr.$new();
        return k; 
        }
}, 0);