function move(){
    const local = localStorage.getItem("keywords")
    let queryParam = local ? `?keywords=${encodeURIComponent(local)}` : "?keywords="; // 값이 있으면 쿼리 파라미터 생성
    window.location.href = `/recommend` + queryParam; // 해당 URL로 이동
}

