<?php

/* DEPENDENCIES */

    require 'db.php';
    $db = new mysqli($host, $dbusername, $dbpassword, $dbname) or die("Connection Error: " . mysqli_error($db));


/*
* Properly encapsulated data within JSON envelope
* Param $arr - array - array of data
* Returns: JSON Object - enveloped data
*
* Author: hudson
*/
function envelopeData($arr){
    $envelope = array("data"=>$arr);
    return json_encode($envelope, JSON_UNESCAPED_SLASHES);
    
}

/* ROUTING */


/**
* Submit an evalutation and set it to active (open) status
* Prereq: Form submission including position and at least
*         one other comment in the likes/dislikes/comments
* Returns: None
*
* Author: hudson
**/
if(isset($_POST['position'])){
    
    $submission = "submission";
    $query = "SELECT * FROM $ConfigTable WHERE config_key='$submission'";
    
    if(!$result = $db->query($query)){
        die(http_response_code(500));
    }
    $arr = array();
    if($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        

        
    }
    if($row['config_value'] == F){
        die(http_response_code(412));
    }
    
    
    
    if($_POST['position'] == ""){
        
        die(http_response_code(417));
    }
    else{
        $name = $db->real_escape_string($_POST["name"]);
        $position = $db->real_escape_string($_POST["position"]);
        
        $likes = $db->real_escape_string($_POST["likes"]);
        
        $dislikes = $db->real_escape_string($_POST["dislikes"]);
        
        $comments = $db->real_escape_string($_POST["comments"]);
        
        $status = "O";
        
        $responses = 0;
        
        if($likes != ""){
            $responses = $responses + 1;
        }
        
        if($dislikes != ""){
            $responses = $responses + 1;
        }
        
        if($comments != ""){
            $responses = $responses + 1;
        }
        
        if($responses == 0){
            die(http_response_code(417));
        }
        
        if($name == ""){
            $name = "Anonymous";
        }
        switch($position){
            case "eboard":
                $position = "Eboard - All";
                break;
            case "chairman":
                $position = "Chairman";
                break;
            case "evals":
                $position = "Evals";
                break;
            case "rd":
                $position = "R&D";
                break;
            case "opcomm":
                $position = "Opcomm";
                break;
            case "imps":
                $position = "House Imps";
                break;
            case "financial":
                $position = "Financial";
                break;
             case "history":
                $position = "History";
                break;
            case "social":
                $position = "Social";
                break;
            
        }
        
        
        
        date_default_timezone_set('EST');
        $date = date("m/d/y");
        
        $query = "INSERT INTO $EvalsTable (name,position,likes,dislikes,comments,status,time) VALUES ('$name','$position','$likes','$dislikes','$comments','$status','$date')";
        
        if(!$result = $db->query($query)){
            
            die(http_response_code(500));
        }
        
    }
    
    http_response_code(200);
    exit;
}


/**
* Get all active evaluations (excluding archived evals)
* Prereq: evals = 'active'
* Returns: JSON Object - array of all eval metadata
*
* Author: hudson
**/
if(isset($_GET['evals']) && $_GET['evals'] == "active"){
    $query = "SELECT * FROM $EvalsTable WHERE status='O' ORDER BY timestamp DESC";
    if(!$result = $db->query($query)){
        http_response_code(500);
        die("RESULT ERROR: " . $db->error.__LINE__);
    }
    $arr = array();
    if($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $arr[] = $row;

        }
    }
    # JSON-encode the response
    $json_response = envelopeData($arr);

    // # Return the response (comes JSON formatted within array)
    echo $json_response;
    http_response_code(200);
    exit;
}


/**
* Archive a given eval by its id
* Prereq: archive = (int) id
* Returns: None
**/
if(isset($_GET['archive'])){
    $id = $db->real_escape_string($_GET['archive']);
    
    $query = "UPDATE $EvalsTable
SET status='A' WHERE eval_id='$id'";
    if(!$result = $db->query($query)){
            
        die(http_response_code(500));
    }
        
    http_response_code(200);
    exit;
    
    
    
}


/**
* Get the current status of submissions
* Returns: JSON Object - current status of submissions
**/
if(isset($_GET['submission']) && $_GET['submission'] == ""){
    $submission = "submission";
    $query = "SELECT * FROM $ConfigTable WHERE config_key='$submission'";
    
    if(!$result = $db->query($query)){
        die($db->error);
    }
    $arr = array();
    if($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $arr[] = $row;

        }
    }
    # JSON-encode the response
    $json_response = envelopeData($arr);

    // # Return the response (comes JSON formatted within array)
    echo $json_response;
    http_response_code(200);
    exit;
    
    
    
}

/**
* Update the status of submissions - open/close
* Prereq: 
*  - submission = 'T' => open submissions
*  or
*  - submission = 'F' => open submissions
*
* Author: hudson
**/
if(isset($_GET['submission']) && $_GET['submission'] != ""){
    $submission = "submission";
    $value = $db->real_escape_string($_GET['submission']);
    $query = "UPDATE $ConfigTable SET config_value='$value' WHERE config_key='$submission'";
    if(!$result = $db->query($query)){
        http_response_code(500);    
        die( $db->error.__LINE__);
    }
        
    http_response_code(200);
    exit;
    
    
}


/**
* Deletes an evaluation based on id
* Prereq: delete = (int) id
* Returns: none
*
* Author: hudson
**/
/*if(isset($_GET['delete'])){
    $id = $db->real_escape_string($_GET['delete']);
    
    $query = "DELETE FROM $EvalsTable WHERE eval_id='$id'";
    if(!$result = $db->query($query)){
            
        die(http_response_code(500));
    }
        
    http_response_code(200);
    exit;
    
    
    
}*/

    

    
    





?>