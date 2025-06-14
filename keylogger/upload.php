<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $safeFileName = basename($_FILES['file']['name']);

    #Dir check
    $uploadDir = __DIR__ . '/upload/';
    if (!file_exists($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }

    #Allowed Ext
    $allowedExt = ['txt'];
    $ext = strtolower(pathinfo($safeFileName, PATHINFO_EXTENSION));
    if (!in_array($ext, $allowedExt)) {
        die("Nope! e");
    }
    #Allowed with MIME
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $mimeType = finfo_file($finfo, $_FILES['file']['tmp_name']);
    finfo_close($finfo);
    $allowedMIME = ['text/plain'];
    if (!in_array($mimeType, $allowedMIME)) {
        die("Nope! m");
    }    
    
    #Strip path
    $timestamp = date('Ymd_His');
    $newName = uniqid('', false) . '.' . $ext;
    $uploadFile = $uploadDir . $timestamp . $newName;
    // var_dump($_FILES['file']);

    if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadFile)) {
        echo "✅ File uploaded successfully: $safeFileName";
    } else {

        echo "❌ Error uploading file.";
    }

    } else {
        echo "⚠️ No file uploaded. Use POST method and ensure 'file' is included.";
    }
?>