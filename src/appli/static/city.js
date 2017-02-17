var arrondissements = {
      75001:{text:"75001 Paris 1er", id:"75101"},
      75002:{text:"75002 Paris 2e", id:"75102"},
      75003:{text:"75003 Paris 3e", id:"75103"},
      75004:{text:"75004 Paris 4e", id:"75104"},
      75005:{text:"75005 Paris 5e", id:"75105"},
      75006:{text:"75006 Paris 6e", id:"75106"},
      75007:{text:"75007 Paris 7e", id:"75107"},
      75008:{text:"75008 Paris 8e", id:"75108"},
      75009:{text:"75009 Paris 9e", id:"75109"},
      75010:{text:"75010 Paris 10e", id:"75110"},
      75011:{text:"75011 Paris 11e", id:"75111"},
      75012:{text:"75012 Paris 12e", id:"75112"},
      75013:{text:"75013 Paris 13e", id:"75113"},
      75014:{text:"75014 Paris 14e", id:"75114"},
      75015:{text:"75015 Paris 15e", id:"75115"},
      75016:{text:"75016 Paris 16e", id:"75116"},
      75017:{text:"75017 Paris 17e", id:"75117"},
      75018:{text:"75018 Paris 18e", id:"75118"},
      75019:{text:"75019 Paris 19e", id:"75119"},
      75020:{text:"75020 Paris 20e", id:"75120"},
      69001:{text:"69001 Lyon 1er", id:"69381"},
      69002:{text:"69002 Lyon 2e", id:"69382"},
      69003:{text:"69003 Lyon 3e", id:"69383"},
      69004:{text:"69004 Lyon 4e", id:"69384"},
      69005:{text:"69005 Lyon 5e", id:"69385"},
      69006:{text:"69006 Lyon 6e", id:"69386"},
      69007:{text:"69007 Lyon 7e", id:"69387"},
      69008:{text:"69008 Lyon 8e", id:"69388"},
      69009:{text:"69009 Lyon 9e", id:"69389"},
      13001:{text:"13001 Marseille 1er", id:"13201"},
      13002:{text:"13002 Marseille 2e", id:"13202"},
      13003:{text:"13003 Marseille 3e", id:"13203"},
      13004:{text:"13004 Marseille 4e", id:"13204"},
      13005:{text:"13005 Marseille 5e", id:"13205"},
      13006:{text:"13006 Marseille 6e", id:"13206"},
      13007:{text:"13007 Marseille 7e", id:"13207"},
      13008:{text:"13008 Marseille 8e", id:"13208"},
      13009:{text:"13009 Marseille 9e", id:"13209"},
      13010:{text:"13010 Marseille 10e", id:"13210"},
      13011:{text:"13011 Marseille 11e", id:"13211"},
      13012:{text:"13012 Marseille 12e", id:"13212"},
      13013:{text:"13013 Marseille 13e", id:"13213"},
      13014:{text:"13014 Marseille 14e", id:"13214"},
      13015:{text:"13015 Marseille 15e", id:"13215"},
      13016:{text:"13016 Marseille 16e", id:"13216"}
    };

$( document ).ready(function() {
    
     /* form submission */
  $("#city_form").submit(function(event){
    $("#id_insee").replaceWith('<input class="vTextField" id="id_insee" maxlength="5" name="insee" required="" type="text" value="'+$("#id_insee").val()+'">');
  });
    $("#id_insee").replaceWith('<select id="id_insee" style="width: 150px;" name="id_insee"></select>');
    $('#id_insee').select2({
      placeholder: "Saisir le code postal",
      selectOnClose: true,
      multiple:false,
      minimumInputLength: 5,
      maximumInputLength: 5,
      language: {
        inputTooShort: function() {
          return false;
        }
      },
      ajax:{
        url: 'https://geo.api.gouv.fr/communes',
        dataType: 'json',
        delay: 250,
        data: function (params) {
          return {
            codePostal: params.term
          };
        },
        processResults: function (data, params) {
          if(arrondissements[params.term]){
            return {
              results:[arrondissements[params.term]]
            }
          }
          return {
            results: data.map(function(item) {
              return {
                id : item.code,
                text : item.codesPostaux+' '+item.nom
              };
            })
          };
        },
        cache: true
        },
        escapeMarkup: function (markup) { return markup; }
    });


});


