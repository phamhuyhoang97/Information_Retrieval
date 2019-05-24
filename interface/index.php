<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" href="bootstrap.min.css">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> -->
<script src="jquery.js"></script>
<style> 
input[type=text] {
  width: 100%;
  box-sizing: border-box;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  background-color: white;
  background-image: url('searchicon.png');
  background-position: 10px 10px; 
  background-repeat: no-repeat;
  padding: 12px 20px 12px 40px;
  -webkit-transition: width 0.4s ease-in-out;
  transition: width 0.4s ease-in-out;
}

input[type=date] {
  width: 100%;
  box-sizing: border-box;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  background-color: white;
  background-image: url('searchicon.png');
  background-position: 10px 10px; 
  background-repeat: no-repeat;
  padding: 12px 20px 12px 40px;
  -webkit-transition: width 0.4s ease-in-out;
  transition: width 0.4s ease-in-out;
}

input[type=text]:focus {
  width: 100%;
}
.col-md-6 button {
	font-size: 20px;
	background-color: white;
	border: none;
}
.row {
	margin-top: 30px;
}

.pagination a {
  color: black;
  float: left;
  padding: 8px 16px;
  text-decoration: none;
  transition: background-color .3s;
}

.pagination a.active {
  background-color: dodgerblue;
  color: white;
}

.pagination a:hover:not(.active) {background-color: #ddd;}
</style>
</head>
<body>
<?php 
	if (isset($_GET['search']) && $_GET['search']) {  // BASIC SEARCH
		// if (getExistData($_GET['search'])) {
		// 	$data = getExistData($_GET['search']);
		// 	$output = $data->value;
		// } else {
		// 	$output = getNewData($_GET['search']);
		// }
		$command = "python /home/hoang/Downloads/InformationRetrieval/src/searchEngine.py -i kenh14 -s '".$_GET['search']."'";
		$stringData = shell_exec($command);
		$output = json_decode($stringData);
	}
	if (isset($_GET['title']) && $_GET['title']) { // ADVANCED SEARCH
		// if (getExistData($_GET['search'])) {
		// 	$data = getExistData($_GET['search']);
		// 	$output = $data->value;
		// } else {
		// 	$output = getNewData($_GET['search']);
		// }
		// time type : yyyy-mm-dd
		$command = "python /home/hoang/Downloads/InformationRetrieval/src/searchEngine.py -i kenh14 -s '".$_GET['search']."'" . " " . $_GET['time'] ;
		$stringData = shell_exec($command);
		$output = json_decode($stringData);
	}
	function getExistData($key) {
		if (file_exists("C:\Users\Hieu\AppData\Local\Google\Chrome\User Data/Profile 4\Cache\keysearch.txt")) {
			$fileData = file_get_contents("C:\Users\Hieu\AppData\Local\Google\Chrome\User Data/Profile 4\Cache\keysearch.txt");
			$dataArray = explode("***", $fileData);
			foreach ($dataArray as $item) {
				$item = json_decode($item);
				if (isset($item->key) && $item->key == $key) {
					return $item;
				}
			}
			return false;
		}
	}
	function getNewData($key) {

		//test _search.json
		// $stringData = file_get_contents("_search.json");

		//  python.py path
		$command = "python /home/hoang/Downloads/InformationRetrieval/src/searchEngine.py -i kenh14 -s '". $key."'";
		$stringData = shell_exec($command);

		
		if ($stringData != '') {
			$jsonData = json_decode($stringData);
			$data = '{"key": "'.$key.'","value": '.$stringData.'}';

			// chrome cache path
			if (file_exists("C:\Users\Hieu\AppData\Local\Google\Chrome\User Data/Profile 4\Cache\keysearch.txt")) {
				$item = "***".$data;
				file_put_contents("C:\Users\Hieu\AppData\Local\Google\Chrome\User Data/Profile 4\Cache\keysearch.txt", $item, FILE_APPEND);
			} else {
				$item = $data;
				$keysearch = fopen("C:\Users\Hieu\AppData\Local\Google\Chrome\User Data/Profile 4\Cache\keysearch.txt", "w");
				fwrite($keysearch, $item);
				fclose($keysearch);
			}
		}
		return $jsonData;
	}
?>
<div class="container">
	<div align="center">
		<h2><a href="testpython.php" style="text-decoration: none;color: green">Elastic Search</a></h2>
	</div>
	<!-- <div class="row" style="margin-top: 20px">
		<div class="col-md-6 col-xs-6" style="padding-right: unset;"><button style="position: absolute; right: 0; border-right: 1px solid red" onclick="showDiv('basic')">Basic</button></div>
		<div class="col-md-6 col-xs-6" style="padding-left: unset;"><button style="" onclick="showDiv('advanced')">Advanced</button></div>
	</div> -->
	<div class="row" style="" id="basic" >
		<div class="col-md-2 col-xs-2"></div>
		<div class="col-md-8 col-xs-8" style="padding-right: unset">
			<form>
				<?php
				$_SESSION['start'] = microtime(true);
					if (isset($_GET['search'])) {
						echo '<input type="text" name="search" placeholder="Search.." id="search" style="" value="'.$_GET['search'].'">';
					} else {
						echo '<input type="text" name="search" placeholder="Search.." id="search" style="">';
					}
				?>
				<button type="submit" name="submit" id="submit" style="padding: 12px 20px 12px 20px;background-color: powderblue; border-radius: 0 5px 5px 0; position: absolute; top: 0; right: 0;border: 2px solid #ccc;">Search</button>
			</form>	
		</div>
		<div class="col-md-2 col-xs-2"></div>
	</div>
	
	<div  align="center">
		
		<div id="suggest"></div>
		
	</div>

	
	<div id="result">
		<?php
			
			if ( isset($output)) {
				$end  = microtime(true);
				$data = $output->hits->hits;
				$totalPages = (count($data))/5;
				$text = '<h5>Có '.count($data).' kết quả tìm được trong 0.000000'.(($end - $_SESSION['start'])*10000000000000000000).' (s).</h5>';
				$text .= '<hr style="width: 100%;color: 2px solid #ccc;">';
				$j =1;
				$total = count($data);

				for($i = 0; $i < $totalPages; $i++) {
					if ($i == 0) {
						$text.='<div class="items" id="page'.($i+1).'">';
					} else {
						$text.='<div class="items" id="page'.($i+1).'" style="display:none">';
					}

					for ($j=0;$j<5;$j++) {
						$index = $i*5 +$j;
						if (isset($data[$index])) {
							$item = $data[$index];
							// print_r($item);die();
							$text .= "<div class='".$item->_id."'><a href='".$item->_source->url."' id='".$j."' onclick='hideItem(this.id);return false;'><h2><b>".$item->_source->title."</b></h2></a><a style='text-decoration:none' href='".$item->_source->url."'><small style='color:blue'>".$item->_source->url."</small></a>";
							$text .= "<div id='content".$j."' style='display:none'><span>".$item->_source->full_content."</span></div>";
							$text .= "<p class='short".$item->_id."'>".$item->_source->short_content."</p><small style='color:#ccc'>".$item->_source->time."</small></div><br>";
						} else break;
					}
					
					$text.= "</div>";
					
						
					
				}
				echo $text;
				echo '<br><div class="pagination">';
				echo '<a href="#" id="1" style="background-color: dodgerblue;" onclick="activeClass(this.id)">1</a>';
				for ($i=2; $i <= $totalPages; $i++) { 
					echo '<a href="#" id="'.$i.'" onclick="activeClass(this.id)">'.$i.'</a>';
				}
				echo '</div>';
			} elseif(isset($_GET['search'])) {
				echo '<div><h2 style="color:#ccc; text-align:center">No results</h2></div>';
			}
		?>
	</div>

	
</div>

<script>
	$( "#search" ).on('keyup',function(e) {
	    if(e.which == 13) {
	        if ($("#search").val() == "" || $("#title").val() == "") {
	        	$( "#submit" ).attr("disabled", "false");
	        	$( "#submit-advanced" ).attr("disabled", "false");
	        } else {
	        	$("#submit"). removeAttr("disabled");
	        	$("#submit-advanced"). removeAttr("disabled");
	        }
	    } else {
	    	// if ($("#search").val() != '') {
	    	// 	$.ajax({
				  //  	url:'ajax.php',
				  //  	data:{key:$("#search").val()},
				  //  	method:'GET',
				  //  	success:function(response){
				  //  		var text = '';
				  //  		if (response != '') {
				  //  			response = response.split("***");
				  //  			var count = response.length;
				  //  			if ( count > 4) {
				  //  				count = 4;
				  //  			}
				  //  			text += '<div style="border:2px solid #ccc;width: 50%;text-align:left">';
				  //  			for (var i = 0; i < count; i++) {
				  //  				if (response[i] != '') {
				  //  					text += '<li style="padding:8px;font-size:16px;margin-left:30px;list-style:none;cursor:pointer"><a href="testpython.php?search='+response[i]+'">'+response[i]+'</a></li>';
				  //  				}
				  //  			}
				  //  			text += '</div>';
				  //  		}
				  //  		document.getElementById("suggest").innerHTML = text;
				  //  	}
			  	// });
	    	// }
	    }

	});
	function hideItem(id) {
		
		for(var i=0; i <10; i++) {
			if (i != id) {
				$("."+i).css("display","none");
				$("#content"+i).removeAttr("style");
				$("#content"+i).css("display","none");
			}
			
			
		}
		
		if ($("#content"+id).css("display") == "block"){
			$("#content"+id).removeAttr("style");
			$("#content"+id).css("display","none");
		} else 	{$("#content"+id).removeAttr("style");$("#content"+id).css("display","block");}
		
	
	}
	function activeClass(id) {
		for(var i=0; i <15; i++) {
			if (i != id) {
				$("#"+i).css("background-color","unset");
				$("#page"+i).css("display","none");
			} else {
				$("#"+i).css("background-color","dodgerblue");
				$("#page"+i).css("display","block");
			}
		}
	}
	window.onload = function() {
		//disable submit with empty key search
		// if ($("#search").val() == "" && $("#title").val() == "") {
	 //        	$( "#submit" ).attr("disabled", "false");
	 //        	$( "#submit-advanced" ).attr("disabled", "false");
	 //        } else {
	 //        	$("#submit"). removeAttr("disabled");
	 //        	$("#submit-advanced"). removeAttr("disabled");
	 //        }
		//
		var params = getSearchParameters();
		// console.log(params.search);
		
		//
	    var hideSuggest = document.getElementById('suggest');
	    document.onclick = function(e) {
	        if(e.target.id !== 'suggest'){
	            hideSuggest.style.display = 'none';
	        } 
	        if(e.target.id == 'search') {
	            hideSuggest.style.display = 'block';
	        } 
	    };
	};
	function showDiv(divId) {
		if (divId == 'basic') {
			$("#advanced").css("display","none");
			$("#basic").css("display","block");
		} else {
			$("#basic").css("display","none");
			$("#advanced").css("display","block");
		}
	}
	function getSearchParameters() {
      var prmstr = window.location.search.substr(1);
      return prmstr != null && prmstr != "" ? transformToAssocArray(prmstr) : {};
	}

	function transformToAssocArray( prmstr ) {
	    var params = {};
	    var prmarr = prmstr.split("&");
	    for ( var i = 0; i < prmarr.length; i++) {
	        var tmparr = prmarr[i].split("=");
	        params[tmparr[0]] = tmparr[1];
	    }
	    return params;
	}
</script>
</body>
</html>
