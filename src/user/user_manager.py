"""用户管理核心模块"""
import json
import os
from exception import AuthenticationError, FileOperationError
from config import USER_DATA_FILE, DEFAULT_USERS
from utils.logger import get_logger

logger = get_logger()

class UserManager:
    """用户管理类"""
    
    def __init__(self):
        """初始化用户管理器"""
        self.users = self._load_users()
    
    def _load_users(self) -> dict:
        """
        加载用户数据
        
        Returns:
            dict: 用户字典，key为用户ID，value为用户信息
        """
        try:
            if os.path.exists(USER_DATA_FILE):
                with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                    users = json.load(f)
                return users
            else:
                # 首次运行，创建默认用户
                default_users_dict = {user['id']: user for user in DEFAULT_USERS}
                self._save_users(default_users_dict)
                return default_users_dict
        except Exception as e:
            logger.error(f"加载用户数据失败: {str(e)}")
            # 加载失败时使用默认用户
            return {user['id']: user for user in DEFAULT_USERS}
    
    def _save_users(self, users: dict):
        """
        保存用户数据
        
        Args:
            users: 用户字典
        """
        try:
            # 确保数据目录存在
            os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
            
            with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存用户数据失败: {str(e)}")
            raise FileOperationError(f"保存用户数据失败: {str(e)}")
    
    def authenticate(self, user_id: str, password: str) -> dict:
        """
        用户认证
        
        Args:
            user_id: 用户ID
            password: 密码
        
        Returns:
            dict: 用户信息
        
        Raises:
            AuthenticationError: 认证失败
        """
        if user_id not in self.users:
            raise AuthenticationError("用户不存在")
        
        if self.users[user_id]['password'] != password:
            raise AuthenticationError("密码错误")
        
        logger.info(f"用户 {user_id} 登录成功")
        return self.users[user_id]
    
    def change_password(self, user_id: str, old_password: str, new_password: str):
        """
        修改密码
        
        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
        
        Raises:
            AuthenticationError: 认证失败
        """
        # 验证旧密码
        if self.users[user_id]['password'] != old_password:
            raise AuthenticationError("旧密码错误")
        
        # 修改密码
        self.users[user_id]['password'] = new_password
        self._save_users(self.users)
        logger.info(f"用户 {user_id} 修改密码成功")
    
    def add_user(self, user_id: str, password: str, role: str):
        """
        添加用户
        
        Args:
            user_id: 用户ID
            password: 密码
            role: 角色
        
        Raises:
            FileOperationError: 操作失败
        """
        if user_id in self.users:
            raise FileOperationError("用户已存在")
        
        self.users[user_id] = {
            'id': user_id,
            'password': password,
            'role': role
        }
        self._save_users(self.users)
        logger.info(f"添加用户 {user_id} 成功")
    
    def delete_user(self, user_id: str):
        """
        删除用户
        
        Args:
            user_id: 用户ID
        
        Raises:
            FileOperationError: 操作失败
        """
        if user_id not in self.users:
            raise FileOperationError("用户不存在")
        
        # 不允许删除默认管理员
        if user_id == 'admin':
            raise FileOperationError("不能删除默认管理员")
        
        del self.users[user_id]
        self._save_users(self.users)
        logger.info(f"删除用户 {user_id} 成功")
    
    def update_user(self, user_id: str, password: str = None, role: str = None):
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            password: 密码（可选）
            role: 角色（可选）
        
        Raises:
            FileOperationError: 操作失败
        """
        if user_id not in self.users:
            raise FileOperationError("用户不存在")
        
        if password:
            self.users[user_id]['password'] = password
        
        if role:
            self.users[user_id]['role'] = role
        
        self._save_users(self.users)
        logger.info(f"更新用户 {user_id} 成功")
    
    def get_all_users(self) -> list:
        """
        获取所有用户
        
        Returns:
            list: 用户列表
        """
        return list(self.users.values())
    
    def get_user(self, user_id: str) -> dict:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
        
        Returns:
            dict: 用户信息
        """
        return self.users.get(user_id)

# 创建全局用户管理器实例
user_manager = UserManager()
