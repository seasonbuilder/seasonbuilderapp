import unittest

from chat_prompt_profiles import (
    build_code_response_kwargs,
    get_box_top_profile,
    get_coach_edge_profile,
)


class ChatPromptProfileTests(unittest.TestCase):
    def test_coach_edge_routes_all_four_app_and_program_combinations(self):
        self.assertEqual(
            get_coach_edge_profile(spiritual=False, program="SB").key,
            "season_builder_values",
        )
        self.assertEqual(
            get_coach_edge_profile(spiritual=False, program="CB").key,
            "culture_builder_values",
        )
        self.assertEqual(
            get_coach_edge_profile(spiritual=True, program="SB").key,
            "season_builder_spiritual",
        )
        self.assertEqual(
            get_coach_edge_profile(spiritual=True, program="CB").key,
            "culture_builder_spiritual",
        )

    def test_unknown_program_defaults_to_season_builder(self):
        profile = get_coach_edge_profile(spiritual=False, program="unexpected")
        self.assertEqual(profile.key, "season_builder_values")

    def test_code_request_has_no_managed_prompt_reference(self):
        request = build_code_response_kwargs(
            profile=get_coach_edge_profile(spiritual=False, program="SB"),
            input_items=[{"role": "user", "content": "Help me grow."}],
            conversation_id="conv_test",
        )
        self.assertNotIn("prompt", request)
        self.assertEqual(request["model"], "gpt-5.6-luna")
        self.assertEqual(request["conversation"], "conv_test")
        self.assertEqual(request["input"][0]["role"], "system")
        self.assertEqual(
            request["tools"][0]["vector_store_ids"],
            ["vs_pSlnhqILn7dfy3rHgTo6fAiB"],
        )

    def test_culture_builder_does_not_enable_file_search(self):
        request = build_code_response_kwargs(
            profile=get_coach_edge_profile(spiritual=True, program="CB"),
            input_items=[{"role": "user", "content": "Help our team."}],
            conversation_id="conv_test",
        )
        self.assertNotIn("tools", request)

    def test_box_top_preserves_low_reasoning_and_file_search(self):
        profile = get_box_top_profile()
        request = build_code_response_kwargs(
            profile=profile,
            input_items=[{"role": "user", "content": "Begin."}],
            conversation_id="conv_test",
        )
        self.assertEqual(profile.reasoning_effort, "low")
        self.assertEqual(
            request["tools"][0]["vector_store_ids"],
            ["vs_68dc1568f9f48191a1d2eb2aa6c469de"],
        )


if __name__ == "__main__":
    unittest.main()
