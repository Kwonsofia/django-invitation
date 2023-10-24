function insertName(elements, text) {
    var cnt = 0;

    while(cnt<elements.length) {
        elements[cnt].innerText = text;
        cnt++;
    }
}

fetch("http://localhost:8000/", {
    "method":"GET",
    credentials: "include"})
    .then(res => res.json())
    .then(res => {
        console.log(res);

        var groom_name = document.querySelectorAll('#groom_name');
        var groom_father_name = document.querySelectorAll('#groom_father_name');
        var groom_mother_name = document.querySelectorAll('#groom_mother_name');
        var bride_name = document.querySelectorAll('#bride_name');
        var bride_father_name = document.querySelectorAll('#bride_father_name');
        var bride_mother_name = document.querySelectorAll('#bride_mother_name');

        insertName(groom_name, res['groom_name']);
        insertName(groom_father_name, res['groom_father_name']);
        insertName(groom_mother_name, res['groom_mother_name']);
        insertName(bride_name, res['bride_name']);
        insertName(bride_father_name, res['bride_father_name']);
        insertName(bride_mother_name, res['bride_mother_name']);
        
        document.getElementById('groom_phone').innerHTML = '<a class="number" href="tel:' + res['groom_phone'] + '">Call</a>';
        document.getElementById('groom_father_phone').innerHTML = '<a class="number" href="tel:' + res['groom_father_phone'] + '">Call</a>';
        document.getElementById('groom_mother_phone').innerHTML = '<a class="number" href="tel:' + res['groom_mother_phone'] + '">Call</a>';
        document.getElementById('bride_phone').innerHTML = '<a class="number" href="tel:' + res['bride_phone'] + '">Call</a>';
        document.getElementById('bride_father_phone').innerHTML = '<a class="number" href="tel:' + res['bride_father_phone'] + '">Call</a>';
        document.getElementById('bride_mother_phone').innerHTML = '<a class="number" href="tel:' + res['bride_mother_phone'] + '">Call</a>';
        document.getElementById('groom_account').innerText = res['groom_account'];
        document.getElementById('groom_father_account').innerText = res['groom_father_account'];
        document.getElementById('bride_account').innerText = res['bride_account'];
        document.getElementById('bride_father_account').innerText = res['bride_father_account'];
        document.getElementById('address').innerText = res['address'];
        document.getElementById('address_tel').innerText = res['address_tel'];
    })
