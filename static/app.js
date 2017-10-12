$(document).ready(function() {

	
	$('a#process').on('click', function(event) {
		$('#successAlert').text('because it\'s the first time we extract this info Wait untill it is done ...').show();
		var flag = '';
		if ($('#downlod_flag').is(":checked"))
			{
			  flag = 1;
			}
		$.ajax({
			data : {
				link : $('#plink').val(),
				download_flag : flag
				
				
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
				var html = '<ul class="container" >'
				for (var i = 0; i < data.rows.length ; i++) {
				    console.log(data.rows[i]);
				    html += '<li><b>The id : </b> '+data.rows[i][0]+' &nbsp <b>The title : </b>'+data.rows[i][2]+' &nbsp <b>The duration : </b> '+data.rows[i][3]+'</li>'
				    //Do something
				}
				html += '</ul>'
				// $('#varConv').text(data.list).show();
				$('#varConv').html(html);
				$('#firstConv').hide();
			}

		});

		event.preventDefault();

	});



});
