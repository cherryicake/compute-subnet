module.exports = {
  apps: [
    {
      name: 'compute-miner-01',
      script: '/workspace/compute-subnet/neurons/miner.py',
      interpreter: '/home/zhousong/anaconda3/envs/compute/bin/python3',
      args: [
        "--axon.port",
        "18801",
        "--netuid",
        "27",
        "--debug",
        "true",
        '--subtensor.chain_endpoint',
        'ws://10.128.0.6:9944',
        '--wallet.name',
        'tianyue_song_01',
        '--wallet.hotkey',
        'hotkey02',
        '--logging.debug',
        // '--logging.trace',
      ],
      autorestart: true,
      watch: false,
      max_memory_restart: '32G',
      env: {
        NODE_ENV: 'production',
      },
      env_production: {
        NODE_ENV: 'production',
      },
    },
  ],
};











