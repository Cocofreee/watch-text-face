plugins {
    alias(libs.plugins.android.application)
}

android {
    enableKotlin = false
    namespace = "com.fernando.textface"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.fernando.textface"
        minSdk = 36
        targetSdk = 36
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        debug {
            isMinifyEnabled = true
        }
        release {
            // TODO: add your own signingConfig here for Play releases.
            isMinifyEnabled = true
            // Never strip WFF resources.
            isShrinkResources = false
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}
