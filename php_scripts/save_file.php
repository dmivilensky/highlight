<?php

$uploaddir = $_SERVER['DOCUMENT_ROOT'].'/files/';
$uploadfile = $uploaddir . basename($_POST['name']);

if (move_uploaded_file($_FILES['document']['tmp_name'], $uploadfile)) {
    echo "OK";
} else {
    echo "ERROR!";
}

?>