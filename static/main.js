function insertName(elements, text) {
    var cnt = 0;

    while(cnt<elements.length) {
        elements[cnt].innerText = text;
        cnt++;
    }
}
