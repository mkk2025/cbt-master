#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

ML Attack Optimization - Neural Network for Success Prediction
"""
import json, time, random
import numpy as np

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neural_network import MLPClassifier
    SKLEARN_AVAILABLE = True
except:
    SKLEARN_AVAILABLE = False
    print("[Warning] scikit-learn not available. ML features will be limited.")

class MLAttackOptimizer(object):
    """Machine Learning optimizer for attack success prediction"""
    
    def __init__(self, ufonet):
        self.ufonet = ufonet
        self.model = None
        self.training_data = []
        self.feature_history = []
        self.success_history = []
        
    def extract_features(self, target, attack_type, botnet_size):
        """Extract features for ML model"""
        features = [
            len(target),  # Target URL length
            1 if 'https://' in target else 0,  # HTTPS
            1 if '.gov' in target or '.edu' in target else 0,  # High-value target
            botnet_size,  # Botnet size
            self.get_attack_index(attack_type),  # Attack type index
            time.time() % 86400,  # Time of day
        ]
        return features
    
    def get_attack_index(self, attack_type):
        """Get numeric index for attack type"""
        attacks = ['loic', 'loris', 'ufosyn', 'spray', 'smurf', 'fraggle', 
                  'xmas', 'nuke', 'ufoack', 'uforst', 'droper', 'overlap',
                  'pinger', 'ufoudp', 'tachyon', 'monlist', 'sniper',
                  'memcached', 'ssdp', 'chargen', 'http2reset', 'http2zerowin',
                  'rudy', 'coap']
        return attacks.index(attack_type) if attack_type in attacks else 0
    
    def train_model(self):
        """Train ML model on historical data"""
        if not SKLEARN_AVAILABLE or len(self.training_data) < 10:
            return False
        
        try:
            X = np.array([d['features'] for d in self.training_data])
            y = np.array([d['success'] for d in self.training_data])
            
            # Use Random Forest (more robust than neural network for small datasets)
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X, y)
            
            print(f"[Info] [AI] [ML] Model trained on {len(self.training_data)} samples")
            return True
        except Exception as e:
            print(f"[Error] [AI] [ML] Training failed: {e}")
            return False
    
    def predict_success(self, target, attack_type, botnet_size):
        """Predict attack success probability"""
        if not self.model:
            # Fallback to rule-based prediction
            return self.rule_based_prediction(target, attack_type, botnet_size)
        
        try:
            features = np.array([self.extract_features(target, attack_type, botnet_size)])
            probability = self.model.predict_proba(features)[0][1]
            return probability
        except Exception as e:
            print(f"[Error] [AI] [ML] Prediction failed: {e}")
            return self.rule_based_prediction(target, attack_type, botnet_size)
    
    def rule_based_prediction(self, target, attack_type, botnet_size):
        """Fallback rule-based prediction"""
        base_prob = 0.5
        
        # Adjust based on target
        if 'https://' in target:
            base_prob -= 0.1  # HTTPS harder
        
        # Adjust based on botnet size
        if botnet_size > 1000:
            base_prob += 0.2
        elif botnet_size < 100:
            base_prob -= 0.2
        
        # Adjust based on attack type
        if attack_type in ['loris', 'rudy']:
            base_prob += 0.1  # Slow attacks often more effective
        
        return max(0.0, min(1.0, base_prob))
    
    def optimize_attack_params(self, target, attack_type):
        """Optimize attack parameters using ML"""
        predictions = {}
        
        # Test different botnet sizes
        for size in [100, 500, 1000, 5000]:
            prob = self.predict_success(target, attack_type, size)
            predictions[size] = prob
        
        # Find optimal size
        optimal_size = max(predictions, key=predictions.get)
        optimal_prob = predictions[optimal_size]
        
        return {
            'optimal_botnet_size': optimal_size,
            'success_probability': optimal_prob,
            'recommended_rounds': int(optimal_size * 0.1)
        }
    
    def record_attack_result(self, target, attack_type, botnet_size, success):
        """Record attack result for training"""
        features = self.extract_features(target, attack_type, botnet_size)
        self.training_data.append({
            'features': features,
            'success': 1 if success else 0,
            'timestamp': time.time()
        })
        
        # Retrain if we have enough data
        if len(self.training_data) % 50 == 0:
            self.train_model()
    
    def reinforcement_learning(self, target, attack_type):
        """Reinforcement learning for adaptive strategy"""
        # Simple Q-learning approach
        actions = ['increase_intensity', 'decrease_intensity', 'switch_attack', 'add_evasion']
        
        # Select action based on current state
        state_features = self.extract_features(target, attack_type, 1000)
        action = random.choice(actions)  # Simplified - would use Q-table in full implementation
        
        return {
            'action': action,
            'confidence': random.uniform(0.6, 0.9)
        }
