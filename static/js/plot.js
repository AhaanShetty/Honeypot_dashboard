$('#top_sig').on('change',function(){
    $.ajax({
        url: "/snort/change",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('top_sig').value
        },
        dataType:"json",
        success: function (data) {
            //alert('Successful');
            console.log('HI')
            Plotly.newPlot('signature_graph', data );
        }
    });
})