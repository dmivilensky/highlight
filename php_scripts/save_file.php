<?php

ini_set('max_execution_time','600');
ini_set('max_input_time','600');
ini_set('memory_limit','1024');
ini_set('post_max_size','1028');	
ini_set('upload_max_filesize','1024');

$uploaddir = $_SERVER['DOCUMENT_ROOT'].'/files/';
$uploadfile = $uploaddir . basename($_POST['name']);

if (move_uploaded_file($_FILES['document']['tmp_name'], $uploadfile)) {
    echo "OK";
} else {
    echo "ERROR!";
}

?>