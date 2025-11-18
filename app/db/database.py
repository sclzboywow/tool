"""
数据库连接和初始化
"""
import sqlite3
import os
from pathlib import Path

# 数据库文件路径
BASE_DIR = Path(__file__).parent.parent.parent
DB_PATH = BASE_DIR / "data" / "fan_database.db"


def get_db():
    """
    获取数据库连接
    
    Returns:
        sqlite3.Connection: 数据库连接
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # 使返回结果为字典格式
    return conn


def init_db():
    """
    初始化数据库，创建表结构
    """
    # 确保data目录存在
    os.makedirs(DB_PATH.parent, exist_ok=True)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 创建风机性能参数表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fan_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fan_type TEXT NOT NULL,
            point_index INTEGER NOT NULL,
            phi REAL NOT NULL,
            psi_p REAL NOT NULL,
            eta REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(fan_type, point_index)
        )
    """)
    
    # 创建索引以提高查询性能
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_fan_type 
        ON fan_performance(fan_type)
    """)
    
    conn.commit()
    conn.close()
    print(f"数据库初始化完成: {DB_PATH}")


def get_fan_performance(fan_type: str):
    """
    获取指定风机型号的性能参数
    
    Args:
        fan_type: 风机型号，如 "4-68"
        
    Returns:
        list: 性能点列表，每个点包含 phi, psi_p, eta
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT point_index, phi, psi_p, eta
        FROM fan_performance
        WHERE fan_type = ?
        ORDER BY point_index ASC
    """, (fan_type,))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return None
    
    # 转换为字典列表
    performance_points = []
    for row in results:
        performance_points.append({
            "phi": row["phi"],
            "psi_p": row["psi_p"],
            "eta": row["eta"]
        })
    
    return performance_points


def insert_fan_performance(fan_type: str, point_index: int, phi: float, psi_p: float, eta: float):
    """
    插入或更新风机性能参数
    
    Args:
        fan_type: 风机型号
        point_index: 性能点序号
        phi: 流量系数
        psi_p: 压力系数
        eta: 效率（百分比，如87.6表示87.6%）
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO fan_performance 
        (fan_type, point_index, phi, psi_p, eta, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (fan_type, point_index, phi, psi_p, eta))
    
    conn.commit()
    conn.close()


def get_all_fan_types():
    """
    获取所有可用的风机型号列表
    
    Returns:
        list: 风机型号列表
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT fan_type
        FROM fan_performance
        ORDER BY fan_type ASC
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    return [row["fan_type"] for row in results]

