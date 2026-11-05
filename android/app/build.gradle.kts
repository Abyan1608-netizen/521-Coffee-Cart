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
        versionCode = 11
        versionName = "1.5.1"
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

    // META-INF/services WAJIB tetap ada (dipakai Firebase/Kotlin coroutines); yang dibuang hanya berkas info/lisensi.
    packaging { resources { excludes += setOf("META-INF/*.version", "META-INF/*.kotlin_module", "META-INF/LICENSE*", "META-INF/NOTICE*",
        "META-INF/DEPENDENCIES", "META-INF/AL2.0", "META-INF/LGPL2.1", "kotlin/**", "**.kotlin_builtins", "DebugProbesKt.bin") } }

    dependenciesInfo {
        includeInApk = false
        includeInBundle = false
    }
}

dependencies {
    // androidx.webkit (WebViewAssetLoader + WebMessageListener). Tanpa AppCompat/Material.
    implementation("androidx.webkit:webkit:1.14.0")
    // Notifikasi instan promo/diskon (Firebase Cloud Messaging). Aktif hanya bila android-web/config.json berisi "fcm".
    implementation(platform("com.google.firebase:firebase-bom:33.7.0"))
    implementation("com.google.firebase:firebase-messaging")
}
