document.addEventListener('DOMContentLoaded', function() {
    // 필터 변경 시 자동 제출
    const filterForm = document.querySelector('.filter-sidebar');
    const filterInputs = filterForm.querySelectorAll('input');
    const sortSelect = document.querySelector('.sort-select');
    
    function applyFilters() {
        const params = new URLSearchParams(window.location.search);
        
        // 현재 선택된 필터값들 수집
        filterInputs.forEach(input => {
            if (input.checked) {
                if (input.type === 'checkbox') {
                    params.append(input.name, input.value);
                } else {
                    params.set(input.name, input.value);
                }
            }
        });
        
        // 정렬 옵션 추가
        params.set('sort', sortSelect.value);
        
        // 페이지 파라미터 제거 (필터 변경시 첫 페이지로)
        params.delete('page');
        
        // URL 업데이트 및 페이지 새로고침
        window.location.search = params.toString();
    }
    
    // 이벤트 리스너 등록
    filterInputs.forEach(input => {
        input.addEventListener('change', applyFilters);
    });
    
    sortSelect.addEventListener('change', applyFilters);
    
    // 필터 초기화
    document.querySelector('.reset-filters').addEventListener('click', function() {
        window.location.href = window.location.pathname;
    });
}); 