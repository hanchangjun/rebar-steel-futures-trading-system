#!/bin/bash

################################################################################
# 螺纹钢期货交易系统 - 快速启动脚本
################################################################################

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 检查 Python 版本
check_python() {
    print_info "检查 Python 版本..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD=python3
    elif command -v python &> /dev/null; then
        PYTHON_CMD=python
    else
        print_error "未找到 Python，请先安装 Python 3.10 或更高版本"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version | awk '{print $2}')
    print_info "Python 版本: $PYTHON_VERSION"
    
    # 检查版本是否 >= 3.10
    MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$MAJOR_VERSION" -lt 3 ] || ([ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -lt 10 ]); then
        print_error "Python 版本过低，需要 3.10 或更高版本"
        exit 1
    fi
    
    print_info "Python 版本检查通过 ✓"
}

# 检查虚拟环境
check_venv() {
    print_info "检查虚拟环境..."
    
    if [ ! -d "venv" ]; then
        print_warning "虚拟环境不存在，正在创建..."
        $PYTHON_CMD -m venv venv
        print_info "虚拟环境创建成功 ✓"
    else
        print_info "虚拟环境已存在 ✓"
    fi
}

# 激活虚拟环境
activate_venv() {
    print_info "激活虚拟环境..."
    source venv/bin/activate
    print_info "虚拟环境已激活 ✓"
}

# 安装依赖
install_dependencies() {
    print_info "检查依赖..."
    
    if [ -f "requirements.txt" ]; then
        print_info "正在安装依赖包..."
        pip install --upgrade pip -q
        pip install -r requirements.txt -q
        print_info "依赖安装完成 ✓"
    else
        print_warning "未找到 requirements.txt 文件"
    fi
}

# 检查端口
check_port() {
    PORT=${1:-5000}
    print_info "检查端口 $PORT..."
    
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "端口 $PORT 已被占用"
        print_info "占用进程："
        lsof -i :$PORT | grep LISTEN
        read -p "是否尝试终止占用进程？(y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            lsof -ti :$PORT | xargs kill -9
            print_info "已终止占用进程 ✓"
        else
            print_info "请手动终止占用进程或更换端口"
            exit 1
        fi
    else
        print_info "端口 $PORT 可用 ✓"
    fi
}

# 启动服务
start_service() {
    PORT=${1:-5000}
    print_info "启动服务（端口 $PORT）..."
    print_info "按 Ctrl+C 停止服务"
    echo ""
    
    python src/main.py -m http -p $PORT
}

# 主函数
main() {
    echo "=========================================="
    echo "  螺纹钢期货交易系统 - 快速启动"
    echo "=========================================="
    echo ""
    
    # 解析参数
    PORT=5000
    SKIP_DEPS=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--port)
                PORT="$2"
                shift 2
                ;;
            --skip-deps)
                SKIP_DEPS=true
                shift
                ;;
            -h|--help)
                echo "用法: $0 [选项]"
                echo ""
                echo "选项:"
                echo "  -p, --port PORT    指定端口号（默认: 5000）"
                echo "  --skip-deps        跳过依赖安装"
                echo "  -h, --help         显示帮助信息"
                echo ""
                echo "示例:"
                echo "  $0                # 使用默认端口 5000"
                echo "  $0 -p 8000        # 使用端口 8000"
                echo "  $0 --skip-deps    # 跳过依赖安装"
                exit 0
                ;;
            *)
                print_error "未知选项: $1"
                echo "使用 -h 或 --help 查看帮助信息"
                exit 1
                ;;
        esac
    done
    
    # 执行检查
    check_python
    check_venv
    activate_venv
    
    if [ "$SKIP_DEPS" = false ]; then
        install_dependencies
    else
        print_info "跳过依赖安装"
    fi
    
    check_port $PORT
    
    # 启动服务
    echo ""
    echo "=========================================="
    echo "  系统准备就绪！"
    echo "=========================================="
    echo ""
    print_info "服务地址: http://localhost:$PORT"
    print_info "API 文档: 参见 API_REFERENCE.md"
    print_info "用户手册: 参见 USER_GUIDE.md"
    echo ""
    
    start_service $PORT
}

# 捕获 Ctrl+C
trap 'echo -e "\n${YELLOW}[INFO] 服务已停止${NC}"; exit 0' INT

# 运行主函数
main "$@"
