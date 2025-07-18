from agents.r_and_d_needs_extractor import extract_rnd_needs
# from message_generator import generate_messages

company = "NKGen Biotech"

# print("== Company's leadership Overview ==")
# print(find_leadership_contact(company))

print("\n== R&D Needs ==")
rnd = extract_rnd_needs(company)
print(rnd)

# print("\n== Contact Info ==")
# contact = find_ceo_contact(company)
# print(contact)

# print("\n== Messages ==")
# print(generate_messages(company, "Dr. Song", "CEO", rnd))
