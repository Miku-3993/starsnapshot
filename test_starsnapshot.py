import unittest
from unittest import mock

import starsnapshot as ss


SAMPLE = [
    {
        "full_name": "owner/alpha",
        "html_url": "https://github.com/owner/alpha",
        "language": "Python",
        "stargazers_count": 500,
        "starred_at": "2026-01-01T00:00:00Z",
    },
    {
        "full_name": "owner/beta",
        "html_url": "https://github.com/owner/beta",
        "language": "Python",
        "stargazers_count": 300,
        "starred_at": "2026-02-01T00:00:00Z",
    },
    {
        "full_name": "owner/gamma",
        "html_url": "https://github.com/owner/gamma",
        "language": "Rust",
        "stargazers_count": 800,
        "starred_at": "2026-03-01T00:00:00Z",
    },
]


class TestFetch(unittest.TestCase):
    def test_pagination(self):
        big = SAMPLE * 34  # 102 items -> two pages (100 + 2) then empty
        pages = [big[:100], big[100:], []]

        def fake_get(url, headers):
            return pages.pop(0)

        with mock.patch.object(ss, "http_get_json", side_effect=fake_get) as m:
            out = ss.fetch_starred("user", {})
        self.assertEqual(len(out), 102)
        self.assertEqual(m.call_count, 2)

    def test_aggregate(self):
        stats = ss.aggregate(SAMPLE)
        self.assertEqual(stats["total"], 3)
        self.assertEqual(dict(stats["by_lang"])["Python"], 2)
        self.assertEqual(stats["top_stars"][0]["full_name"], "owner/gamma")
        self.assertEqual(stats["recent"][0]["full_name"], "owner/gamma")


class TestRender(unittest.TestCase):
    def test_render_empty(self):
        text = ss.render("someone", ss.aggregate([]))
        self.assertIn("**Total starred repositories: 0**", text)
        self.assertIn("No starred repositories yet", text)

    def test_render_content(self):
        text = ss.render("user", ss.aggregate(SAMPLE))
        self.assertIn("owner/gamma", text)
        self.assertIn("## By language", text)
        self.assertIn("| Python | 2 |", text)


class TestHeaders(unittest.TestCase):
    def test_token_in_headers(self):
        with mock.patch.dict("os.environ", {"GH_TOKEN": "sekret"}, clear=False):
            headers = ss.build_headers()
        self.assertEqual(headers["Authorization"], "Bearer sekret")

    def test_no_token(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            headers = ss.build_headers()
        self.assertNotIn("Authorization", headers)


if __name__ == "__main__":
    unittest.main()