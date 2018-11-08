
var accounts = ["acc0", "acc1", "acc2"];
$.each(accounts, function(index, value) {
	$("#account").append($('<option>').text(value).attr('value', index));
});


$(function() {
	$('#account').change(function() {
		this.form.submit();
	});
});
