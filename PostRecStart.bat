@echo off
chcp 932 > nul

rem // �E�C���h�E���\���ɂ���
rem _EDCBX_HIDE_

rem // �p�����[�^�����ϐ��ɓn��
rem // �������邱�Ƃ� Python ���ł����ϐ����Q�Ƃł���
rem _EDCBX_DIRECT_

rem // �����\��Ȃ�I��
if "%RecMode%" == "4" (
    goto :eof
)

rem // EDCBNotifier.exe �����s
python %~dp0\EDCBNotifier\EDCBNotifier.exe PostRecStart

exit
