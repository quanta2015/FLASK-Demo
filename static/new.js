$(init)

function init() {
  $('input[name="m-date"]').daterangepicker({
    singleDatePicker: true
  });


  $('body').on('change','#uploadFile',doUpload)


  $('body').on('click','#codeBtn',doCode)
  $('body').on('click','#linkBtn',linkBtn)
  $('body').on('click','#listBtn',listBtn)
  $('body').on('click','#h1Btn',h1Code)
  $('body').on('click','#h2Btn',h2Code)
  $('body').on('click','#h3Btn',h3Code)
}


function doCode() {
  cnt = document.getElementById('cnt');
  val = `\`\`\`javascript\n\n\n\`\`\``
  insertAtCursor(cnt, val )
}

function linkBtn() {
  cnt = document.getElementById('cnt');
  val = `[](http://....)\n`
  insertAtCursor(cnt, val )
}

function listBtn() {
  cnt = document.getElementById('cnt');
  val = `- xxx\n- xxx\n- xxx\n`
  insertAtCursor(cnt, val )
}

function h1Code() {
  cnt = document.getElementById('cnt');
  insertAtCursor(cnt, `# ` )
}

function h2Code() {
  cnt = document.getElementById('cnt');
  insertAtCursor(cnt, `## ` )
}

function h3Code() {
  cnt = document.getElementById('cnt');
  insertAtCursor(cnt, `### ` )
}


function doUpload() {
  var file = $("#uploadFile")[0].files[0];
  var form = new FormData();
  form.append("file", file);

  $.ajax({
    url: "/uploadImg/",
    type: "POST",
    data: form,
    async: true,
    processData: false,
    contentType: false,
    success: function(result) {
        cnt = document.getElementById('cnt');
        ret = JSON.parse(result)
        val = `![img](${ret.filename})`
        insertAtCursor(cnt, val )
    }
  });
}


function insertAtCursor(obj, val) {
    if (document.selection) {
        //IE support
        obj.focus();
        sel = document.selection.createRange();
        sel.text = val;
        sel.select();
    } else if (obj.selectionStart || obj.selectionStart == '0') {
        //MOZILLA/NETSCAPE support
        var startPos = obj.selectionStart;
        var endPos = obj.selectionEnd;
        var beforeValue = obj.value.substring(0, startPos);
        var afterValue = obj.value.substring(endPos, obj.value.length);

        obj.value = beforeValue + val + afterValue;

        obj.selectionStart = startPos + val.length;
        obj.selectionEnd = startPos + val.length;
        obj.focus();
    } else {
        obj.value += val;
        obj.focus();
    }
}