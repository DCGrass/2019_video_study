// 先判断视频区域的状态 默认是false 如果不存在 即false,那么显示,并将当前状态变为true
// 如果是存在的 就代表当前视频编辑区域是显示出来的 就将其hide() 隐藏,并将当前状态变为false
var videoEreaStatic = false;
var videoEditArea = $('#video-edit-area');

$('#open-add-video-btn').click(function(){
    if (!videoEreaStatic) {
        videoEditArea.show();
        videoEreaStatic = true;
    } else {
        videoEditArea.hide();
        videoEreaStatic = false;
    }
});