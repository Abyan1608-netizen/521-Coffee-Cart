import java.util.Properties

plugins {
    id("com.android.application")
}

// Kunci tanda tangan rilis dibaca dari android/keystore.properties (JANGAN di-commit / dibagikan).
val ksFile = rootProject.file("keystore.properties")
val ks = Properties().apply { if (ksFile.exists()) ksFile.inputStream().use { load(it) } }

android {
    namespace = "id.coffee521.pos"
    compileSdk = 36

    defaultConfig {
        applicationId = "id.coffee521.pos"
        minSdk = 26          // Android 8.0+
        targetSdk = 36       // wajib Play Store sejak 31 Agustus 2026
        versionCode = 2
        versionName = "1.1.0"
    }

    signingConfigs {
        if (ksFile.exists()) {
            create("release") {
                storeFile = rootProject.file(ks.getProperty("storeFile"))
                storePassword = ks.getProperty("storePassword")
                keyAlias = ks.getProperty("keyAlias")
                keyPassword = ks.getProperty("keyPassword")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true        // R8: kecilkan & samarkan kode
            isShrinkResources = true      // buang resource yang tak terpakai
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            if (ksFile.exists()) signingConfig = signingConfigs.getByName("release")
        }
        debug {
            applicationIdSuffix = ".debug"
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures { buildConfig = true }

    // File web sudah kecil/terkompresi; jangan kompres ulang foto & font.
    androidResources { noCompress += listOf("jpg", "png", "woff") }

    packaging { resources { excludes += setOf("META-INF/**", "kotlin/**", "**.kotlin_builtins", "DebugProbesKt.bin") } }

    dependenciesInfo {
        includeInApk = false
        includeInBundle = false
    }
}

dependencies {
    // Satu-satunya dependensi: androidx.webkit (WebViewAssetLoader + WebMessageListener). Tanpa AppCompat/Material/Kotlin.
    implementation("androidx.webkit:webkit:1.14.0")
}
