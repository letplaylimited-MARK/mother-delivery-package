"""QCM 三模式入口 — research / production / service"""
import sys, os, json, time, logging

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from qcm.config import QCMConfig, load_config
from qcm.pipeline import PipelineEngine

logger = logging.getLogger(__name__)


HEADER = """
================================================================
  QCM 22-Formula Pipeline
  Mode: {mode}  |  Plugins: {plugins}  |  Roles: {roles}
================================================================
"""


def setup_logging(level):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def format_round(r, max_r):
    bar = "#" * int(r * 30) + "." * (30 - int(r * 30))
    return f"R={r:.4f} |{bar}|"


def print_research(result, plugins_active):
    comps = f"K={result.components.get('K_sim',0):.3f} C={result.components.get('C_comp',0):.3f} I={result.components.get('I_freq',0):.3f}"
    extra = ""
    for key in plugins_active:
        if key in result.enhanced:
            if key == 'epr':
                extra += f" epr={result.enhanced['epr'].get('entanglement',0):.3f}"
            elif key == 'kgrowth':
                extra += f" kg={result.enhanced['kgrowth'].get('knowledge',0):.2f}"
            elif key == 'rcs':
                extra += f" rcs={result.enhanced['rcs'].get('score',0):.3f}"
            elif key == 'dw':
                extra += " dw"
    if 'crypto' in result.enhanced:
        extra += " cap-d"
    if 'healer' in result.enhanced:
        extra += " cap-g"
    print(f"  Round {result.round:3d}: {result.R:.4f} -> {result.level}{extra}")
    if result.round <= 3 or result.round % 10 == 0:
        print(f"         {comps}")


def run_research(config):
    print(HEADER.format(mode="RESEARCH", plugins=config.active_plugins, roles=config.role_names))
    engine = PipelineEngine(config)
    for rnd in range(config.max_rounds):
        result = engine.run_round()
        print_research(result, config.active_plugins)
    report = engine.get_report()
    print("\n" + "=" * 64)
    print(f"  EMERGENCE: {'YES at R=' + str(report.r_at_emergence) if report.emergence_occurred else 'NO'}")
    print(f"  Rounds: {report.total_rounds}  |  Max R: {report.max_R:.4f}  |  Avg R: {report.avg_R:.4f}")
    print("=" * 64)
    return report


def run_production(config):
    engine = PipelineEngine(config)
    report = engine.run()
    result = {
        "emergence": report.emergence_occurred,
        "r_at_emergence": report.r_at_emergence,
        "total_rounds": report.total_rounds,
        "max_R": report.max_R,
        "avg_R": round(report.avg_R, 4),
        "final_R": report.final_R,
    }
    output_dir = config.get("output.dir", "output")
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"qcm_result_{int(time.time())}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"  Result saved to {path}")
    print(f"  EMERGENCE: {result['emergence']}  |  Rounds: {result['total_rounds']}  |  Max R: {result['max_R']:.4f}")
    return report


def run_service(config):
    logger.info("Starting QCM HTTP service...")
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel
        import uvicorn
    except ImportError:
        print("  [ERROR] fastapi/uvicorn required: pip install fastapi uvicorn")
        return

    app = FastAPI(title="QCM Pipeline Service", version="6.3")

    engine_ctx = {"current": None}

    class SimulateRequest(BaseModel):
        rounds: int = 10
        roles: list = ["Secretary", "Researcher"]
        seed: int = 42
        plugins: list = []
        capabilities: dict = {}

    @app.get("/health")
    def health():
        return {"status": "healthy", "service": "QCM Pipeline", "version": "6.3"}

    @app.get("/status")
    def status():
        return {"service": "QCM Pipeline", "version": "6.3", "status": "running"}

    @app.post("/simulate")
    def simulate(req: SimulateRequest):
        cfg = QCMConfig({
            "roles": req.roles,
            "seed": req.seed,
            "max_rounds": req.rounds,
            "mode": "production",
        })
        if req.plugins:
            cfg.set("plugins", {p: True for p in req.plugins})
        if req.capabilities:
            cfg.set("capabilities", req.capabilities)
        engine = PipelineEngine(cfg)
        report = engine.run()
        return {
            "emergence": report.emergence_occurred,
            "r_at_emergence": report.r_at_emergence,
            "total_rounds": report.total_rounds,
            "max_R": report.max_R,
            "final_R": report.final_R,
        }

    @app.post("/step")
    def step():
        if engine_ctx["current"] is None:
            cfg = QCMConfig({"max_rounds": 100, "mode": "production"})
            engine_ctx["current"] = PipelineEngine(cfg)
        result = engine_ctx["current"].run_round()
        return {
            "round": result.round,
            "R": result.R,
            "level": result.level,
            "emergence": result.emergence_occurred,
        }

    @app.post("/reset")
    def reset():
        engine_ctx["current"] = None
        return {"status": "reset"}

    @app.get("/history")
    def history():
        if engine_ctx["current"] is None:
            return {"rounds": []}
        return {
            "total_rounds": engine_ctx["current"].round_count,
            "rounds": [
                {"round": r.round, "R": r.R, "level": r.level}
                for r in engine_ctx["current"].rounds_log[-50:]
            ],
        }

    @app.post("/capabilities")
    def capabilities(data: dict):
        if engine_ctx["current"] is None:
            return {"error": "no active engine"}
        cfg = engine_ctx["current"].config
        if "crypto" in data:
            cfg.set("capabilities.crypto", data["crypto"])
        if "healer" in data:
            cfg.set("capabilities.healer", data["healer"])
        engine_ctx["current"]._init_capabilities()
        return {"capabilities": {"crypto": engine_ctx["current"].crypto is not None, "healer": engine_ctx["current"].healer is not None}}

    port = int(config.get("service.port", 8080))
    logger.info("Listening on http://0.0.0.0:%d", port)
    uvicorn.run(app, host="0.0.0.0", port=port)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="QCM 22-Formula Pipeline")
    parser.add_argument("--mode", choices=["research", "production", "service"], default="research",
                        help="Run mode (default: research)")
    parser.add_argument("--config", type=str, default=None,
                        help="Path to config file (.json or .yaml)")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed (overrides config)")
    parser.add_argument("--roles", type=str, nargs="*", default=None,
                        help="Role names (overrides config)")
    parser.add_argument("--max-rounds", type=int, default=None,
                        help="Maximum rounds (overrides config)")
    parser.add_argument("--port", type=int, default=None,
                        help="Service port (service mode only)")
    parser.add_argument("--output", type=str, default=None,
                        help="Output directory (production mode)")
    parser.add_argument("--log-level", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        help="Logging level (default: INFO)")
    parser.add_argument("--plugins", type=str, nargs="*", default=None,
                        help="Enable specific plugins (overrides config)")
    parser.add_argument("--cap-crypto", action="store_true",
                        help="Enable Cap-D CryptoEngine")
    parser.add_argument("--cap-healer", action="store_true",
                        help="Enable Cap-G SelfHealer")
    args = parser.parse_args()

    setup_logging(args.log_level)

    if args.config:
        config = load_config(args.config)
    else:
        config = QCMConfig()
    config.set("mode", args.mode)

    if args.seed is not None:
        config.set("seed", args.seed)
    if args.roles:
        config.set("roles", args.roles)
    if args.max_rounds is not None:
        config.set("max_rounds", args.max_rounds)
    if args.port is not None:
        config.set("service.port", args.port)
    if args.output is not None:
        config.set("output.dir", args.output)
    if args.plugins is not None:
        config.set("plugins", {p: True for p in args.plugins})
    if args.cap_crypto:
        config.set("capabilities.crypto", True)
    if args.cap_healer:
        config.set("capabilities.healer", True)

    modes = {
        "research": run_research,
        "production": run_production,
        "service": run_service,
    }
    modes[args.mode](config)


if __name__ == "__main__":
    main()
