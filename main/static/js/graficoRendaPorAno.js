$(function () {
    var $rendaChart2 = $("#grafico_renda_por_ano");
      $.ajax({
        url: $rendaChart2.data("url"),
        success: function (data) {

          var ctx = $rendaChart2[0].getContext("2d");

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Total de Renda por Ano',
                backgroundColor:'blue',
                
                data: data.data
              }]          
            },
            options: {
              responsive: true,
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Renda por Ano'
            }
        }
      });

    }
  });

});
