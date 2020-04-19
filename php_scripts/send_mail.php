<?php

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;

require './PHPMailer/Exception.php';
require './PHPMailer/PHPMailer.php';
require './PHPMailer/SMTP.php';

$ini = parse_ini_file('php.ini');

$mail = new PHPMailer;
$mail->isSMTP();
$mail->SMTPDebug = SMTP::DEBUG_SERVER;
$mail->CharSet = "UTF-8";

$mail->Host = 'smtp.gmail.com';
$mail->Port = 587;
$mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;

$mail->SMTPAuth = true;
$mail->Username = $ini['user'];
$mail->Password = $ini['pwd'];

$mail->setFrom($ini['user'], 'HighLight');
$mail->addAddress($_GET['email'], '');
$mail->Subject = 'HighLight: документ '.$_GET['name'];

$mail->Body = 'Документ прислан сайтом highlight.spb.ru';
$mail->addAttachment('../'.$_GET['path']);

if (!$mail->send()) {
    echo 'Mailer Error: '. $mail->ErrorInfo;
} else {
    echo 'Message sent!';
}

?>