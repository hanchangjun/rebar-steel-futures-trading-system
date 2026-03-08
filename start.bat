@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ################################################################################
REM 螺纹钢期货交易系统 - 快速启动脚本 (Windows)
REM ################################################################################

set "PORT=5000"
set "SKIP_DEPS=false"

REM 解析参数
:parse_args
if "%~1"=="" goto end_parse_args
if /i "%~1"=="-p" (
    set "PORT=%~2"
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--port" (
    set "PORT=%~2"
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--skip-deps" (
    set "SKIP_DEPS=true"
    shift
    goto parse_args
)
if /i "%~1"=="-h" goto show_help
if /i "%~1"=="--help" goto show_help
echo [错误] 未知选项: %~1
goto usage

:show_help
echo 用法: %~nx0 [选项]
echo.
echo 选项:
echo   -p, --port PORT    指定端口号（默认: 5000）
echo   --skip-deps        跳过依赖安装
echo   -h, --help         显示帮助信息
echo.
echo 示例:
echo   %~nx0              # 使用默认端口 5000
echo   %~nx0 -p 8000      # 使用端口 8000
echo   %~nx0 --skip-deps  # 跳过依赖安装
exit /b 0

:usage
echo 使用 -h 或 --help 查看帮助信息
exit /b 1

:end_parse_args

echo ==========================================
echo   螺纹钢期货交易系统 - 快速启动
echo ==========================================
echo.

REM 检查 Python
echo [INFO] 检查 Python 版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.10 或更高版本
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python 版本: %PYTHON_VERSION%

REM 检查虚拟环境
echo [INFO] 检查虚拟环境...
if not exist "venv\" (
    echo [警告] 虚拟环境不存在，正在创建...
    python -m venv venv
    echo [INFO] 虚拟环境创建成功 ✓
) else (
    echo [INFO] 虚拟环境已存在 ✓
)

REM 激活虚拟环境
echo [INFO] 激活虚拟环境...
call venv\Scripts\activate.bat
echo [INFO] 虚拟环境已激活 ✓

REM 安装依赖
if "%SKIP_DEPS%"=="false" (
    echo [INFO] 检查依赖...
    if exist "requirements.txt" (
        echo [INFO] 正在安装依赖包...
        pip install --upgrade pip -q
        pip install -r requirements.txt -q
        echo [INFO] 依赖安装完成 ✓
    ) else (
        echo [警告] 未找到 requirements.txt 文件
    )
) else (
    echo [INFO] 跳过依赖安装
)

REM 检查端口
echo [INFO] 检查端口 %PORT%...
netstat -ano | findstr ":%PORT% " >nul 2>&1
if not errorlevel 1 (
    echo [警告] 端口 %PORT% 已被占用
    echo [INFO] 占用进程：
    netstat -ano | findstr ":%PORT% "
    set /p KILL_PROCESS="是否尝试终止占用进程？(y/n): "
    if /i "!KILL_PROCESS!"=="y" (
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%PORT% "') do (
            taskkill /F /PID %%a >nul 2>&1
        )
        echo [INFO] 已终止占用进程 ✓
    ) else (
        echo [INFO] 请手动终止占用进程或更换端口
        pause
        exit /b 1
    )
) else (
    echo [INFO] 端口 %PORT% 可用 ✓
)

REM 启动服务
echo.
echo ==========================================
echo   系统准备就绪！
echo ==========================================
echo.
echo [INFO] 服务地址: http://localhost:%PORT%
echo [INFO] API 文档: 参见 API_REFERENCE.md
echo [INFO] 用户手册: 参见 USER_GUIDE.md
echo.
echo [INFO] 启动服务（端口 %PORT%）...
echo [INFO] 按 Ctrl+C 停止服务
echo.

python src/main.py -m http -p %PORT%

pause
