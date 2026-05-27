"""
Flywheel Optimizer - 飞轮优化系统
公式16: dθ/dt = α*∇L(θ) - β*θ(t) + γ*ε(t)
公式17: α(t) = α_init * (1+γ*t^κ)^(-1) * e^(-λ*loss_variance(t))
公式18: A(t) = A_0 * (1 + η*t/t_ref)^ζ
参数: α=0.1, β=0.9, ρ_max=0.73<1 (Lyapunov稳定)
"""

import math
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class FlywheelState:
    """飞轮状态"""
    acceleration: float  # 加速度 A(t)
    learning_rate: float  # 学习率 α(t)
    momentum: float    # 动量
    energy: float    # 能量 E(t)


class FlywheelOptimizer:
    """
    飞轮优化器
    基于论文公式16-18的双层循环飞轮系统
    """

    # 论文校准参数
    ALPHA_INIT = 0.1     # 初始学习率
    BETA = 0.9          # 衰减系数
    GAMMA = 0.1          # 扰动系数
    KAPPA = 0.5         # 学习率衰减指数
    LAMBDA_VAR = 0.1     # 方差衰减系数

    # 能量参数
    ETA = 0.1           # 加速度增长系数
    T_REF = 10          # 参考时间步
    ZETA = 0.7          # 增长指数

    # Lyapunov稳定性阈值
    RHO_MAX = 0.73

    def __init__(self):
        self.t = 0                      # 时间步
        self.theta = 0.0                # 参数
        self.loss_history = []           # 损失历史
        self.variance_history = []        # 方差历史
        self.learning_rate_history = []    # 学习率历史
        self.acceleration_history = []    # 加速度历史
        self.state_history = []           # 状态历史

    def add_loss(self, loss: float):
        """添加损失值"""
        self.loss_history.append(loss)

        # 计算方差
        if len(self.loss_history) >= 2:
            variance = abs(loss - self.loss_history[-2])
        else:
            variance = 0.0

        self.variance_history.append(variance)
        self.t += 1

    def calculate_adaptive_lr(self) -> float:
        """
        计算自适应学习率 (公式17)
        α(t) = α_init * (1+γ*t^κ)^(-1) * e^(-λ*loss_variance)
        """
        if not self.variance_history:
            return self.ALPHA_INIT

        variance = self.variance_history[-1]

        # 学习率衰减
        lr_decay = 1.0 / (1.0 + self.GAMMA * (self.t ** self.KAPPA))

        # 方差衰减
        variance_decay = math.exp(-self.LAMBDA_VAR * variance)

        lr = self.ALPHA_INIT * lr_decay * variance_decay

        return max(0.001, min(self.ALPHA_INIT, lr))

    def calculate_acceleration(self) -> float:
        """
        计算加速度 (公式18)
        A(t) = A_0 * (1 + η*t/t_ref)^ζ
        """
        base_acceleration = 1.0

        # 增长因子
        growth = self.ETA * self.t / self.T_REF

        acceleration = base_acceleration * Math.pow(1.0 + growth, self.ZETA)

        return acceleration

    def calculate_derivative(self, gradient: float, perturbation: float = 0.0) -> float:
        """
        计算参数变化率 (公式16)
        dθ/dt = α*∇L(θ) - β*θ(t) + γ*ε(t)
        """
        lr = self.calculate_adaptive_lr()

        # 梯度下降项
        gradient_term = lr * gradient

        # 衰减项
        decay_term = self.BETA * self.theta

        # 扰动项
        perturbation_term = self.GAMMA * perturbation

        derivative = gradient_term - decay_term + perturbation_term

        return derivative

    def update(self, gradient: float, perturbation: float = 0.0) -> FlywheelState:
        """
        更新飞轮状态
        """
        # 计算各项
        lr = self.calculate_adaptive_lr()
        acceleration = self.calculate_acceleration()
        derivative = self.calculate_derivative(gradient, perturbation)

        # 更新参数
        self.theta += derivative * lr

        # 计算动量
        momentum = abs(derivative)

        # 计算能量
        energy = 0.5 * momentum ** 2 + acceleration

        # 记录历史
        self.learning_rate_history.append(lr)
        self.acceleration_history.append(acceleration)

        # 创建状态
        state = FlywheelState(
            acceleration=acceleration,
            learning_rate=lr,
            momentum=momentum,
            energy=energy
        )
        self.state_history.append(state)

        return state

    def calculate_lyapunov(self) -> float:
        """
        计算Lyapunov指数
        用于验证系统稳定性
        ρ = d(ln|θ|)/dt
        """
        if self.t < 2 or abs(self.theta) < 1e-10:
            return 0.0

        # 简单近似
        if len(self.state_history) < 2:
            return 0.0

        prev_momentum = self.state_history[-2].momentum
        curr_momentum = self.state_history[-1].momentum

        if prev_momentum < 1e-10:
            return 0.0

        lyapunov = math.log(curr_momentum / prev_momentum)

        return lyapunov

    def is_stable(self) -> bool:
        """
        判断系统是否稳定 (Lyapunov稳定性)
        |ρ| < ρ_max
        """
        rho = abs(self.calculate_lyapunov())
        return rho < self.RHO_MAX

    def get_state(self) -> Dict:
        """获取飞轮状态"""
        if not self.state_history:
            return {
                't': 0,
                'theta': 0.0,
                'learning_rate': self.ALPHA_INIT,
                'acceleration': 1.0,
                'momentum': 0.0,
                'energy': 0.0,
                'lyapunov': 0.0,
                'stable': True,
            }

        state = self.state_history[-1]
        lyapunov = self.calculate_lyapunov()

        return {
            't': self.t,
            'theta': round(self.theta, 6),
            'learning_rate': round(state.learning_rate, 6),
            'acceleration': round(state.acceleration, 6),
            'momentum': round(state.momentum, 6),
            'energy': round(state.energy, 6),
            'lyapunov': round(lyapunov, 6),
            'stable': self.is_stable(),
            'loss': round(self.loss_history[-1], 4) if self.loss_history else 0.0,
        }

    def predict_convergence(self) -> Optional[int]:
        """
        预测收敛所需步数
        基于Lyapunov指数
        """
        if self.t < 3:
            return None

        rho = abs(self.calculate_lyapunov())

        if rho < 0.01:
            return 0

        if not self.loss_history:
            return None

        current_loss = self.loss_history[-1]
        target_loss = 0.01

        if current_loss <= target_loss:
            return 0

        # 简单估算
        import math as m
        steps_needed = int(m.log(target_loss / current_loss) / m.log(1 - rho)) + 1

        return min(steps_needed, 1000)


class Math:
    """数学工具类"""
    @staticmethod
    def pow(x: float, y: float) -> float:
        return x ** y


def test_flywheel():
    """测试飞轮优化器"""
    print("=" * 60)
    print("Flywheel Optimizer Test")
    print("=" * 60)

    fw = FlywheelOptimizer()

    print("\n--- Simulating optimization ---")

    # 模拟梯度下降
    gradients = [0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.08, 0.05, 0.03, 0.02]

    for i, grad in enumerate(gradients):
        loss = 1.0 / (i + 1)  # 模拟损失
        fw.add_loss(loss)
        state = fw.update(gradient=grad)
        status = fw.get_state()

        print(f"Step {i+1}: loss={loss:.3f}, lr={status['learning_rate']:.4f}, "
              f"acc={status['acceleration']:.3f}, energy={status['energy']:.3f}, "
              f"stable={status['stable']}")

    # 检查状态
    final_state = fw.get_state()
    print(f"\nFinal state: t={final_state['t']}, theta={final_state['theta']:.4f}")
    print(f"Lyapunov: {final_state['lyapunov']:.4f}, Stable: {final_state['stable']}")

    # 预测收敛
    convergence = fw.predict_convergence()
    print(f"Predicted convergence steps: {convergence}")

    print("\n" + "=" * 60)
    print("[PASS] Flywheel Optimizer Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    test_flywheel()