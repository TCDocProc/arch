<?php
// ===========================================
// Conors <==> Kawaii OpenEMR Integration
// ==
// PLEASE NOTE: THIS INTEGRATION REQUIRES A FULLY INSTALLED KAWAII OPENEMR
// It WILL NOT work with any other installation.
// ==
// Place this file in the root OpenEMR web folder, 
// usually /var/www/site, but may vary depending on your 
// installation.
// ===========================================

header('Content-Type: application/json');

// Path to pathways, with trailing slash
$file_path = "interface/patient_file/carepathway/pathway/";

// ===========================================
// Do Not Edit Below this line
// ===========================================

$site_id = 'default';
$ignoreAuth = true;
require_once "sites/$site_id/sqlconf.php";
require_once('interface/globals.php');
require_once("library/authentication/common_operations.php");   
require_once('library/authentication/login_operations.php');

class DocProcApi {
    public function __construct() {
        if (isset($_GET['call']) && $_GET['call'] == 'check_login') {
            $this->check_user($_POST['username'], $_POST['password']);
        }
    }

    public function validate_user_password($username, $password) {
        $authorizedPortal=false; //flag

        DEFINE("TBL_PAT_ACC_ON","patient_access_onsite");
        DEFINE("COL_PID","pid");
        DEFINE("COL_POR_PWD","portal_pwd");
        DEFINE("COL_POR_USER","portal_username");
        DEFINE("COL_POR_SALT","portal_salt");
        DEFINE("COL_POR_PWD_STAT","portal_pwd_status");
        $sql= "SELECT ".implode(",",array(COL_ID,COL_PID,COL_POR_PWD,COL_POR_SALT,COL_POR_PWD_STAT))
              ." FROM ".TBL_PAT_ACC_ON
              ." WHERE ".COL_POR_USER."=?";
        $auth = privQuery($sql, array($username));
        if ( oemr_password_hash($password, $auth[COL_POR_SALT]) == $auth[COL_POR_PWD] ) {
            return $auth[COL_PID];
        } else {
            return -1;
        }
    }

    // This function exists because the kawakii team files are not full PEOS files, but just processes.
    public function fix_process_file($username, $file) {
        return "<peos>
    <models>
        <model>clinical_assessment</model>
    </models>
    " . $file . "</peos>";
    }

    public function check_user($username, $password) {
        $a = array();
        $id = $this->validate_user_password($username, $password);
        if ($id != -1) {
            $a['login_success'] = true;
            $myfile = fopen($GLOBALS['file_path'].$id.".dat.xml", "r") or die("Unable to open file! ".$GLOBALS['file_path'].$id.".dat.xml");
            $lol = fread($myfile,filesize($GLOBALS['file_path'].$id.".dat.xml"));
            fclose($myfile);
            $a['xml'] = $this->fix_process_file($username, $lol);
        } else {
            $a['login_success'] = false;
        }
        
        echo(json_encode($a));
    }
}

$api = new DocProcApi();
?>