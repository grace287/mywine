document.addEventListener("DOMContentLoaded", function () {
    window.showNoteDetail = function(noteId) {
        fetch(`/notes/note_detail/${noteId}/`)  // 노트 데이터를 가져오는 API 엔드포인트
            .then(response => {
                if (!response.ok) {
                    throw new Error('노트 데이터를 불러오는 데 실패했습니다.');
                }
                return response.json();
            })
            .then(note => {
                // 모달의 각 요소를 업데이트
                document.getElementById('note-wine-name').textContent = note.wine_name;
                document.getElementById('note-winery').textContent = note.winery || '정보 없음';
                document.getElementById('note-vintage').textContent = note.vintage || '정보 없음';
                document.getElementById('note-tasting-date').textContent = note.tasting_date || '정보 없음';
                document.getElementById('note-overall').textContent = note.overall || '정보 없음';

                // 모달 표시
                const modal = document.getElementById('note-detail-modal');
                modal.style.display = 'block';
            })
            .catch(error => {
                console.error('노트 상세 정보 로드 중 오류:', error);
                alert('노트 상세 정보를 불러오는 중 오류가 발생했습니다.');
            });
    };

    // 모달 닫기 기능
    const closeButton = document.querySelector('.close-button');
    closeButton.addEventListener('click', function () {
        const modal = document.getElementById('note-detail-modal');
        modal.style.display = 'none';
    });

    // 모달 외부를 클릭하면 닫기
    window.addEventListener('click', function (event) {
        const modal = document.getElementById('note-detail-modal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});











// function showNoteDetail(noteId) {
//     fetch(`/notes/api/note/${noteId}/`)
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('노트를 불러오는 데 실패했습니다.');
//             }
//             return response.json();
//         })
//         .then(note => {
//             document.getElementById('note-wine-name').textContent = note.wine_name;
//             document.getElementById('note-winery').textContent = note.winery;
//             document.getElementById('note-vintage').textContent = note.vintage;
//             document.getElementById('note-tasting-date').textContent = note.tasting_date;
//             document.getElementById('note-overall').textContent = note.overall;
//             document.getElementById('note-sweetness').textContent = note.sweetness; // 추가
//             document.getElementById('note-acidity').textContent = note.acidity; // 추가
//             document.getElementById('note-tannin').textContent = note.tannin; // 추가
//             document.getElementById('note-body').textContent = note.body; // 추가

//             document.getElementById('note-detail-modal').style.display = 'block';
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             alert('노트를 불러오는 데 오류가 발생했습니다.');
//         });
// }