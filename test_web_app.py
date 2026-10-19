#!/usr/bin/env python3
"""Automated unit test suite for GhostVault Web GUI & API endpoints."""

import unittest
import threading
import time
import urllib.request
import urllib.error
import json
import socketserver
from web_app import GhostVaultHandler, PORT, APP_STATE

TEST_PORT = 8799

class TestGhostVaultWebApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        socketserver.TCPServer.allow_reuse_address = True
        cls.server = socketserver.TCPServer(("127.0.0.1", TEST_PORT), GhostVaultHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.2)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_01_index_page(self):
        url = f"http://127.0.0.1:{TEST_PORT}/"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            body = resp.read().decode("utf-8")
            self.assertIn("GhostVault Pro", body)
            self.assertIn("Cloudflare R2", body)
            self.assertIn("Stop Paying Google", body)

    def test_02_status_api(self):
        url = f"http://127.0.0.1:{TEST_PORT}/api/status"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(data.get("ok"))
            self.assertIn("app", data)
            self.assertEqual(data["app"], "GhostVault Pro")

    def test_03_audit_api(self):
        url = f"http://127.0.0.1:{TEST_PORT}/api/audit"
        req = urllib.request.Request(url, data=b"{}", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(data.get("ok"))
            self.assertIn("used_mb", data)
            self.assertIn("free_gb", data)
            self.assertIn("quota_pct", data)

    def test_04_archive_simulation_api(self):
        url = f"http://127.0.0.1:{TEST_PORT}/api/archive/simulate"
        payload = json.dumps({"destination": "Cloudflare R2 ($0 Egress)"}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(data.get("ok"))
            self.assertEqual(data.get("divergence"), 0)
            self.assertEqual(data.get("drive_objects"), 266)
            self.assertEqual(data.get("email_objects"), 20)

    def test_05_pro_activation_api(self):
        url = f"http://127.0.0.1:{TEST_PORT}/api/pro/activate"
        # Test valid key
        payload = json.dumps({"license_key": "GV-PRO-LIFETIME"}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(data.get("ok"))
            self.assertEqual(data.get("tier"), "Pro Lifetime")

        # Test invalid key
        payload_bad = json.dumps({"license_key": "bad"}).encode("utf-8")
        req_bad = urllib.request.Request(url, data=payload_bad, headers={"Content-Type": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req_bad)
        self.assertEqual(ctx.exception.code, 400)

    def test_06_manifest_api(self):
        url = f"http://127.0.0.1:{TEST_PORT}/api/manifest"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data.get("divergence_bytes"), 0)
            self.assertEqual(data.get("verification_method"), "SHA256+MD5")

if __name__ == "__main__":
    unittest.main()
