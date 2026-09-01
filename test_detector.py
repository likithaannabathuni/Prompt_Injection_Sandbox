from detector import detect_prompt_injection


prompt = input(
    "Enter a prompt to test: "
)


result = detect_prompt_injection(
    prompt
)


print("\n================================")
print("PROMPT INJECTION DETECTION")
print("================================")

print(
    f"Probability: "
    f"{result['probability']:.4f}"
)

print(
    f"Risk Score: "
    f"{result['risk_score']:.2f}/100"
)

print(
    f"Classification: "
    f"{result['classification']}"
)